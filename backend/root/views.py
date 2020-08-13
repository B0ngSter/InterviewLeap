from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import pytz
from authentication.models import Skill, CandidateProfile, Interview, InterviewerProfile, InterviewSlots
from io import BytesIO
from django.core.mail import EmailMultiAlternatives
from django.http import BadHeaderError, HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from root.serializers import BookInterviewCreateSerializer, SKillSearchSerializer, PaymentSerializer
import requests
from instamojo_wrapper import Instamojo
from .models import PaymentDetails, BookInterview, PaymentStatusLog
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import hmac
from hashlib import sha1
import datetime
from django.db import transaction, IntegrityError
import xhtml2pdf.pisa as pisa

api = Instamojo(api_key=settings.PAYMENT_API_KEY, auth_token=settings.PAYMENT_AUTH_TOKEN, endpoint=settings.INSTAMOJO_TESTING_URL)


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
        total_amount = payment_amount + (payment_amount*tax)/100
        response = {
                    "timezone_list": pytz.all_timezones,
                    "amount": settings.CUSTOM_PAYMENT_AMOUNT,
                    "tax": int(round(payment_amount*tax)/100),
                    "total_amount": round(total_amount)
                    }

        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        interview_dict = request.data
        tax = settings.TAX_PERCENTAGE
        payment_amount = settings.CUSTOM_PAYMENT_AMOUNT
        tax_amount = (payment_amount * tax) / 100
        total_amount = payment_amount + (payment_amount * tax) / 100
        link = "{frontend_url}/book-interview".format(frontend_url=settings.FRONTEND_URL)
        webhook_url = "{domain}/webhook/payment-response/".format(domain=settings.WEBHOOK_STAGING_URL)
        response = api.payment_request_create(
            amount=total_amount,
            purpose='Interview Leap',
            send_email=True,
            email=self.request.user.email,
            redirect_url=link,
            webhook=webhook_url
        )
        cleaned_data = {"payment_request_id": response['payment_request']['id'],
                        "amount": response['payment_request']['amount'],
                        "email": self.request.user.email,
                        "created_at": response['payment_request']['created_at']
                        # "tax_amount": tax_amount
                        }

        interview_dict['candidate'] = request.user.id
        if 'skills' in interview_dict:
            interview_dict['skills'] = [{'title': skill} for skill in interview_dict['skills'].split(",")]
        interview_dict['time_slots'] = interview_dict['time_slots']
        serializer = self.get_serializer(data=interview_dict)
        long_url = response['payment_request']['longurl']
        if serializer.is_valid():
            serializer.save()
            cleaned_data['interview_slug'] = serializer.data['slug']
            payment_serializer = PaymentSerializer(data=cleaned_data)
            if payment_serializer.is_valid():
                payment_serializer.save()
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
            "logo_url": '',
            "email": email,
            "discount_amount": 0
        }
        subject = 'Payment Invoice for Interview Leap!'
        email_plaintext_message = render_to_string('emailer/payment_success_mail.html', context)

        stn = render_to_string("emailer/invoice.html", context=context, request=request)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(stn.encode("utf-8")), result)
        msg = EmailMultiAlternatives(
            subject,
            "",
            send_by,
            [email]
        )
        msg.attach_alternative(email_plaintext_message, 'text/html')
        msg.attach('invoice.pdf', result.getvalue(), 'application/pdf')
        msg.send()
        print("mail sent***")

    except BadHeaderError:
        return Response({"message":'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)


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
            try:
                with transaction.atomic():
                    check_payment = PaymentStatusLog.objects.filter(payment_request_id=data['payment_request_id']).first()
                    data['other_detail'] = {"fees": data.pop('fees'), "long_url": data.pop('longurl'), "short_url": data.pop('shorturl')}
                    tax = settings.TAX_PERCENTAGE
                    data['tax_amount'] = (data['amount'] * tax) / 100
                    payment_obj, created = PaymentDetails.objects.get_or_create(**data)
                    payment_obj.save()
                    # payment_details = api.payment_request_payment_status(payment_obj.payment_request_id, payment_obj.payment_id)
                    # payment_data = {"instrument_type": payment_details['instrument_type'], "billing_instrument": payment_details['billing_instrument']}
                    # payment_obj.__dict__.update(**payment_data)
                    book_interview = BookInterview.objects.filter(slug=check_payment.interview_slug).first()
                    book_interview.is_payment_done = True
                    book_interview.payment_detail = PaymentDetails.objects.filter(payment_request_id=data['payment_request_id']).first()
                    book_interview.save()
                    check_payment.delete()
                    send_mail_on_subscription(request, payment_obj.buyer, payment_obj.buyer_name, payment_obj.amount, book_interview.slug, payment_obj.created_at, payment_obj.tax_amount, payment_obj.amount)
                    # send mail, update calculate tax, instrument, billing
            except IntegrityError:
                transaction.rollback()
        else:
            payment_log_obj = PaymentStatusLog.objects.filter(payment_request_id=data['payment_request_id']).first()
            payment_log_obj.status = "Failed"
            payment_log_obj.save(update_fields=['status'])
        return HttpResponse(200)
    else:
        payment_log_obj = PaymentStatusLog.objects.filter(payment_request_id=data['payment_request_id']).first()
        payment_log_obj.status = "Failed-400"
        payment_log_obj.save(update_fields=['status'])
        #check for HTTPResponseRedirect
        return HttpResponse(400)


class CandidateDashboardView(ListAPIView):
    queryset = Interview.objects.all()
    # pagination_class = 10

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        mock_list = []
        for data in queryset:
            profile_obj = InterviewerProfile.objects.filter(user=data.interviewer).first()
            mock_list.append({"job_title": data.job_title,
                              "company": profile_obj.company if profile_obj else '',
                              "exp_years": profile_obj.exp_years if profile_obj else '',
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


class MockBookingView(APIView):

    def get(self, request, *args, **kwargs):
        mock_slug = kwargs.get('slug')
        tax = settings.TAX_PERCENTAGE
        payment_amount = Interview.objects.get(slug=mock_slug).quoted_price
        payment_amount = int(payment_amount)
        total_amount = payment_amount + (payment_amount * tax) / 100
        response = {
            "timezone_list": pytz.all_timezones,
            "amount": settings.CUSTOM_PAYMENT_AMOUNT,
            "tax": int(round(payment_amount * tax) / 100),
            "total_amount": round(total_amount)
        }
        return Response(response, status=status.HTTP_200_OK)

    def _date_time_naive_format(self, date, time):
        date_time = date + ' ' + time
        naive = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        return naive

    def post(self, request, *args, **kwargs):
        mock_slug = kwargs.get('slug')
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        start_date_time = self._date_time_naive_format(date, start_time)
        end_date_time = self._date_time_naive_format(date, end_time)
        slot_obj = InterviewSlots.objects.filter(interview__slug=mock_slug,
                                                 interview_start_time=start_date_time,
                                                 interview_end_time=end_date_time,
                                                 candidate=None
                                                 )
        if slot_obj.exists():
            payment_amount = int(slot_obj.first().interview.quoted_price)
            tax = settings.TAX_PERCENTAGE
            total_amount = payment_amount + (payment_amount * tax) / 100
            link = "{frontend_url}/dashboard".format(frontend_url=settings.FRONTEND_URL)
            webhook_url = "{domain}/webhook/mock-interview/".format(domain=settings.WEBHOOK_STAGING_URL)
            response = api.payment_request_create(
                amount=total_amount,
                purpose='Interview Leap mock',
                send_email=True,
                email=self.request.user.email,
                redirect_url=link,
                webhook=webhook_url
            )
            cleaned_data = {"payment_request_id": response['payment_request']['id'],
                            "amount": response['payment_request']['amount'],
                            "email": self.request.user.email,
                            "created_at": response['payment_request']['created_at'],
                            'interview_slug': mock_slug}

            payment_serializer = PaymentSerializer(data=cleaned_data)
            if payment_serializer.is_valid():
                payment_serializer.save()
                long_url = response['payment_request']['longurl']
                return Response({"long_url": long_url}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Some server error happen."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "The slot you are trying to book is already booked by someone else, Please try another slot"},
                            status=status.HTTP_200_OK)


@require_POST
@csrf_exempt
def mock_booking_webhook_handler(request):
    data = request.POST.dict()
    mac_provided = data.pop('mac')
    message = "|".join(v for k, v in sorted(data.items(), key=lambda x: x[0].lower()))
    message = bytes(message, 'utf-8')
    SALT = bytes(settings.PAYMENT_SALT, 'utf-8')
    mac_calculated = hmac.new(SALT, message, sha1).hexdigest()
    if mac_provided == mac_calculated:
        if data['status'] == "Credit":
            try:
                with transaction.atomic():
                    payment_log = PaymentStatusLog.objects.filter(payment_request_id=data['payment_request_id']).first()
                    data['other_detail'] = {"fees": data.pop('fees'), "long_url": data.pop('longurl'), "short_url": data.pop('shorturl')}
                    tax = settings.TAX_PERCENTAGE
                    amount = int(float(data['amount']))
                    tax = round(amount * tax)/100
                    data['tax_amount'] = str(tax)
                    payment_obj, created = PaymentDetails.objects.get_or_create(**data)
                    payment_obj.save()
                    # update calculate tax, instrument, billing
                    #chceck time slot also
                    mock_interview = InterviewSlots.objects.filter(interview__slug=payment_log.interview_slug).first()
                    mock_interview.is_payment_done = True
                    mock_interview.candidate = CandidateProfile.objects.get(user__email=payment_log.email)
                    mock_interview.payment_detail = PaymentDetails.objects.get(payment_request_id=data['payment_request_id'])
                    mock_interview.save()
                    payment_log.delete()
                    send_mail_on_subscription(request, payment_obj.buyer, payment_obj.buyer_name, payment_obj.amount,
                                              mock_interview.interview.slug, payment_obj.created_at, payment_obj.tax_amount,
                                              payment_obj.amount)
            except IntegrityError:
                transaction.rollback()
        else:
            payment_log_obj = PaymentStatusLog.objects.filter(payment_request_id=data['payment_request_id']).first()
            payment_log_obj.status = "Failed"
            payment_log_obj.save(update_fields=['status'])
        return HttpResponse(200)
    else:
        payment_log_obj = PaymentStatusLog.objects.filter(payment_request_id=data['payment_request_id']).first()
        payment_log_obj.status = "Failed-400"
        payment_log_obj.save(update_fields=['status'])
        return HttpResponse(400)
