from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import pytz
from authentication.models import Skill, InterviewSlots
from authentication.serializers import InterviewerRequestsListSerializer
from root.serializers import BookInterviewCreateSerializer, SKillSearchSerializer, FeedbackCreateViewSerializer
from io import BytesIO
from django.core.mail import EmailMultiAlternatives
from django.http import BadHeaderError, HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from root.serializers import BookInterviewCreateSerializer, PaymentSerializer
import requests
from instamojo_wrapper import Instamojo
from .models import PaymentDetails, BookInterview
from authentication.models import Interview, InterviewerProfile
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import hmac
from hashlib import sha1
from django.utils import timezone
from datetime import datetime

# import xhtml2pdf.pisa as pisa

api = Instamojo(api_key=settings.PAYMENT_API_KEY, auth_token=settings.PAYMENT_AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/')


class BookInterviewView(CreateAPIView):
    """
        Book Interview   -- Authenticated Candidate can create/book interview  they are willing to interviewed!
        actions -- Post -- Book Interview
        Request params -- {
                    "company_type": "product","service","captive" (string)
                    "skills": (string)
                    "applied_designation" : "python developer" (string)
                    "date": "2020-06-21", (string)
                    "time_slots": [
                            "9am - 10am",
                            "2pm - 3pm"
                            "6pm - 7pm",
                    ] (array field)
                }
        Response Status -- 200 Ok along with booking interview details
        Error Code -- 400 Bad Request
        Error message -- Raise proper error messages
    """

    serializer_class = BookInterviewCreateSerializer

    def get(self, request, *args, **kwargs):
        tax = settings.TAX_PERCENTAGE
        payment_amount = settings.CUSTOM_PAYMENT_AMOUNT
        total_amount = payment_amount + (payment_amount * tax) / 100
        response = {
            "timezone_list": pytz.all_timezones,
            "amount": settings.CUSTOM_PAYMENT_AMOUNT,
            "tax": int(round(payment_amount * tax) / 100),
            "total_amount": round(total_amount)
        }

        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        interview_dict = request.data.dict()
        tax = settings.TAX_PERCENTAGE
        payment_amount = settings.CUSTOM_PAYMENT_AMOUNT
        tax_amount = (payment_amount * tax) / 100
        total_amount = payment_amount + (payment_amount * tax) / 100
        link = "{frontend_url}/book-interview".format(frontend_url=settings.FRONTEND_URL)
        response = api.payment_request_create(
            amount=total_amount,
            purpose='Interview Leap',
            send_email=True,
            email=self.request.user.email,
            redirect_url=link,
            webhook=""
        )
        cleaned_data = {"payment_request_id": response['payment_request']['id'],
                        "amount": response['payment_request']['amount'],
                        "tax_amount": tax_amount
                        }
        payment_serializer = PaymentSerializer(data=cleaned_data)
        if payment_serializer.is_valid():
            payment_serializer.save()

        interview_dict['candidate'] = request.user.id
        if 'skills' in interview_dict:
            interview_dict['skills'] = [{'title': skill} for skill in interview_dict['skills'].split(",")]
        interview_dict['time_slots'] = interview_dict['time_slots'].split(',')
        interview_dict['payment_detail'] = PaymentDetails.objects.get(
            payment_request_id=response['payment_request']['id']).id
        serializer = self.get_serializer(data=interview_dict)
        long_url = response['payment_request']['longurl']

        if serializer.is_valid():
            serializer.save()
            return Response({"long_url": long_url}, status=status.HTTP_200_OK)
        else:
            if serializer.errors.get('message'):
                error_message = serializer.errors.get('message')[0]
            else:
                error_message = ", ".join([error for error in serializer.errors.keys()])
                error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class TimeSlotListView(APIView):
    """
       Retrieve -- Retrieve list of time slots.
       Actions -- GET method
       Response Status -- 200 Ok
    """

    def get(self, request, *args, **kwargs):
        time_slots = settings.CANDIDATE_TIME_SLOTS
        slots = [slot[0] for slot in time_slots]
        return Response({"time_slot": slots}, status=status.HTTP_200_OK)


def send_mail_on_subscription(request, email, full_name, amount, invoice_number, paid_on, tax, total_amount):
    try:

        send_by = settings.DEFAULT_FROM_EMAIL
        context = {
            "full_name": full_name,
            "amount": amount,
            "invoice_number": invoice_number,
            "paid_on": paid_on,
            "tax": tax,
            "coupon_code": '',
            "total_amount": total_amount,
            "logo_url": settings.STATIC_ROOT + '/img/logo.png',
            "email": email,
            "discount_amount": 0
        }
        subject = 'Welcome to Equiv+ family!'
        # email_plaintext_message = render_to_string('emailer/subscription_success_mail.html', context)

        stn = render_to_string("emailer/invoice.html", context=context, request=request)
        result = BytesIO()
        pdf = ''
        # pdf = pisa.pisaDocument(BytesIO(stn.encode("utf-8")), result)
        msg = EmailMultiAlternatives(
            subject,
            "",
            send_by,
            [email]
        )
        # msg.attach_alternative(email_plaintext_message, 'text/html')
        msg.attach('invoice.pdf', result.getvalue(), 'application/pdf')

        msg.send()
        print("mail sent***")

    except BadHeaderError:
        return Response({"message": 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)


@require_POST
@csrf_exempt
def mojo_handler(request):
    data = request.POST.dict()
    mac_provided = data.pop('mac')
    message = "|".join(v for k, v in sorted(data.items(), key=lambda x: x[0].lower()))
    message = bytes(message, 'utf-8')
    SALT = bytes(settings.PAYMENT_SALT, 'utf-8')
    mac_calculated = hmac.new(SALT, message, sha1).hexdigest()
    if mac_provided == mac_calculated:
        if data['status'] == "Credit":
            payment_obj = PaymentDetails.objects.filter(payment_request_id=data['payment_request_id']).first()
            payment_obj.__dict__.update(**data)
            payment_obj.save()
            book_interview = BookInterview.objects.filter(
                payment_detail__payment_request_id=data['payment_request_id']).first()
            book_interview.is_payment_done = True
            book_interview.save(update_fields=['is_payment_done'])

        else:
            payment_obj = PaymentDetails.objects.filter(payment_request_id=data['payment_request_id']).first()
            payment_obj.status = "Failed"
            payment_obj.save(update_fields=['status'])
            # send mail
        return HttpResponse(200)
    else:
        return HttpResponse(400)


class CandidateInterviewerDashboardView(ListAPIView):
    """
               Retrieve -- Retrieve dashboard detaisl based on the role.
               For Interviewer:
               Actions -- GET method
               Response Status -- 200 Ok
               Response sample dict -- {
                        "new_interview_requests": 1,
                        "interview_created": 1,
                        "interview_taken": 1,
                        "total_earnings": 1,
                        "interview_requests": {
                        "applied_designation": null,
                        "time_slots": [],
                        "date": datetime,
                        "candidate": FK,
                        }
            }
            For Candidate:

        """
    queryset = Interview.objects.all()
    serializer_class = InterviewerRequestsListSerializer
    pagination_class = 10

    def get(self, request, *args, **kwargs):
        if request.user.role == 'Interviewer':
            dashboard_details = {}
            skills = InterviewerProfile.objects.get(user=self.request.user).skills.values_list('title', flat=True)
            interviews_created = InterviewSlots.objects.filter(interview__interviewer=request.user)
            interviews_taken = interviews_created.filter(candidate__isnull=False,
                                                         interview_end_time__lt=timezone.now())
            interview_requests = BookInterview.objects.filter(candidate__isnull=True, date__gte=timezone.now())
            for skill in skills:
                interview_requests = interview_requests.filter(skills__title__icontains=skill)
            dashboard_details['new_interview_requests'] = interview_requests.count()
            dashboard_details['interview_created'] = interviews_created.count()
            dashboard_details['interview_taken'] = interviews_taken.count()
            dashboard_details['total_earnings'] = 0  # need to implement
            interview_requests_serialize = self.get_serializer(interview_requests, many=True).data
            dashboard_details['interview_requests'] = interview_requests_serialize
            return Response(dashboard_details, status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            mock_list = []
            for data in queryset:
                profile_obj = InterviewerProfile.objects.get(user=data.interviewer)
                mock_list.append({"job_title": data.job_title,
                                  "company": profile_obj.company,
                                  "exp_years": profile_obj.exp_years,
                                  })

            return Response({"mocks": mock_list}, status=status.HTTP_200_OK)


class SkillSearchView(ListAPIView):
    pagination_class = None
    queryset = Skill.objects.all()
    serializer_class = SKillSearchSerializer

    def get(self, request, *args, **kwargs):
        if 'search' in request.GET.keys():
            skills = self.request.GET.get('search')
            result = Skill.objects.filter(title__iregex=r'(' + skills + ')')
            output_res = [item.title for item in result]
            if len(output_res) > 0:
                return Response({"result": output_res}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No skill with this key found!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Missing parameter."}, status=status.HTTP_400_BAD_REQUEST)


class CandidateInterviewFeedbackView(CreateAPIView):
    serializer_class = FeedbackCreateViewSerializer

    def create(self, request, *args, **kwargs):

        """
                   Detail -- Interviewer can provide feedback for interview which he/she participated.
                   Actions -- Post method
                   Response Status -- 200 Ok
                   Request dict --
                                    {"date":"2020-08-10",
                                    "start_time":"13:00",
                                    "end_time":"14:00",
                                    "feedback":{"technical_skill":"Exceptional","communication_skill":"Exceptional",
                                    "presentation_skill":"Exceptional","understanding_of_role":"Exceptional",
                                    "text":"nice interview", "strength":"coding skills",
                                    "limitations":"understanding the problem","consider_for_job":"yes"}}
        """

        interview_info = request.data
        interview_info['start_time'] = date_time_naive_format(request.data['date'],
                                                              request.data['start_time'])
        interview_info['end_time'] = date_time_naive_format(request.data['date'], request.data['end_time'])
        interview_slot = InterviewSlots.objects.get(interview__slug=kwargs['slug'],
                                                    interview__interviewer=self.request.user,
                                                    interview_start_time=interview_info['start_time'],
                                                    interview_end_time=interview_info['end_time'])
        serializer = self.get_serializer(interview_slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Thank you for your Feedback"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Some issue occurred while providing Feedback"},
                            status=status.HTTP_400_BAD_REQUEST)


def date_time_naive_format(date, time):
    date_time = date + ' ' + time
    naive = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
    return naive
