from django.conf import settings
from django.db.models import Q
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
from root.serializers import BookInterviewCreateSerializer, SKillSearchSerializer, PaymentSerializer, BookInterviewUpdateSerializer
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
from backend.decorators import profile_complete
from django.shortcuts import HttpResponseRedirect, reverse
import json

api = Instamojo(api_key=settings.PAYMENT_API_KEY,
                auth_token=settings.PAYMENT_AUTH_TOKEN,
                endpoint=settings.INSTAMOJO_URL)


@method_decorator(profile_complete, name='dispatch')
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
                        "created_at": response['payment_request']['created_at'],
                        "tax_amount": tax_amount
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
                    check_payment = PaymentStatusLog.objects.get(payment_request_id=data['payment_request_id'])
                    data['tax_amount'] = check_payment.tax_amount
                    # headers = {"X-Api-Key": settings.PAYMENT_API_KEY,
                    #            "X-Auth-Token": settings.PAYMENT_AUTH_TOKEN}
                    # url = '{}/payments/{}/'.format(settings.INSTAMOJO_URL, data['payment_id'])
                    # response_data = requests.get(url, headers=headers)
                    # payment_details = json.loads(response_data.text)
                    # data['instrument_type'] = payment_details['payment']['instrument_type']
                    # data['billing_instrument'] = payment_details['payment']['billing_instrument']
                    # data['payout_id'] = payment_details['payment']['payout']['id']
                    # data['payout_at'] = payment_details['payment']['payout']['paid_out_at']
                    data['other_detail'] = {"fees": data.pop('fees'),
                                            "long_url": data.pop('longurl'),
                                            "short_url": data.pop('shorturl'),
                                            # "payment_details": payment_details
                                            }
                    payment_obj, created = PaymentDetails.objects.get_or_create(**data)
                    payment_obj.save()
                    book_interview = BookInterview.objects.filter(slug=check_payment.interview_slug).first()
                    book_interview.is_payment_done = True
                    book_interview.payment_detail = PaymentDetails.objects.filter(payment_request_id=data['payment_request_id']).first()
                    book_interview.save()
                    check_payment.delete()
                    send_mail_on_subscription(request, payment_obj.buyer, payment_obj.buyer_name, payment_obj.amount,
                                              book_interview.slug, payment_obj.created_at, payment_obj.tax_amount,
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
                              "slug": data.slug
                              })
        custom_booking_obj = BookInterview.objects.filter(is_payment_done=True)
        booking_list = []
        for each_row in custom_booking_obj:
            booking_list.append({"date": each_row.date, "job_title": each_row.applied_designation, "slug": each_row.slug})

        response = {"mocks": mock_list, "upcoming_interviews": booking_list}

        return Response(response, status=status.HTTP_200_OK)


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


@method_decorator(profile_complete, name='dispatch')
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
                                                 candidate__isnull=True
                                                 )
        if slot_obj.exists():
            payment_amount = int(slot_obj.first().interview.quoted_price)
            tax = settings.TAX_PERCENTAGE
            tax_amount = (payment_amount * tax) / 100
            total_amount = payment_amount + (payment_amount * tax) / 100
            link = "{frontend_url}/dashboard".format(frontend_url=settings.FRONTEND_URL)
            webhook_url = "{domain}/webhook/mock-interview/".format(domain=settings.WEBHOOK_STAGING_URL)
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
                            "created_at": response['payment_request']['created_at'],
                            'interview_slug': mock_slug,
                            "start_time": start_date_time,
                            "end_time": end_date_time,
                            "tax_amount": tax_amount
                            }

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
                    payment_log = PaymentStatusLog.objects.get(payment_request_id=data['payment_request_id'])
                    data['tax_amount'] = payment_log.tax_amount
                    # headers = {"X-Api-Key": settings.PAYMENT_API_KEY,
                    #            "X-Auth-Token": settings.PAYMENT_AUTH_TOKEN}
                    # url = '{}/payments/{}/'.format(settings.INSTAMOJO_URL, data['payment_id'])
                    # response_data = requests.get(url, headers=headers)
                    # payment_details = json.loads(response_data.text)
                    # data['instrument_type'] = payment_details['payment']['instrument_type']
                    # data['billing_instrument'] = payment_details['payment']['billing_instrument']
                    # data['payout_id'] = payment_details['payment']['payout']['id']
                    # data['payout_at'] = payment_details['payment']['payout']['paid_out_at']
                    data['other_detail'] = {"fees": data.pop('fees'),
                                            "long_url": data.pop('longurl'),
                                            "short_url": data.pop('shorturl'),
                                            # "payment_details": payment_details
                                            }
                    payment_obj, created = PaymentDetails.objects.get_or_create(**data)
                    payment_obj.save()
                    mock_interview = InterviewSlots.objects.get(interview__slug=payment_log.interview_slug,
                                                                interview_start_time=payment_log.start_time,
                                                                interview_end_time=payment_log.end_time)
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
            payment_log_obj = PaymentStatusLog.objects.get(payment_request_id=data['payment_request_id'])
            payment_log_obj.status = "Failed"
            payment_log_obj.save(update_fields=['status'])
        return HttpResponse(200)
    else:
        payment_log_obj = PaymentStatusLog.objects.get(payment_request_id=data['payment_request_id'])
        payment_log_obj.status = "Failed-400"
        payment_log_obj.save(update_fields=['status'])
        return HttpResponse(400)


class CustomBookInterviewUpdateView(RetrieveUpdateAPIView):
    """
            Update Book Interview   -- Authenticated Candidate can update their interview
            actions -- Patch -- Book Interview
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
            Error message -- Raise with error messages
    """

    serializer_class = BookInterviewUpdateSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        booking_obj = BookInterview.objects.get(slug=self.kwargs['slug'])
        response = BookInterviewUpdateSerializer(booking_obj).data
        return Response(response, status=status.HTTP_200_OK)

    def get_object(self):
        interviewer = BookInterview.objects.get(slug=self.kwargs['slug'])
        return interviewer

    def update(self, request, *args, **kwargs):
        interview_dict = request.data
        booking_obj = self.get_object()
        if 'skills' in interview_dict:
            interview_dict['skills'] = [{'title': skill} for skill in interview_dict['skills'].split(",")]
        serializer = self.get_serializer(booking_obj, data=interview_dict, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your booking has been updated successfully"}, status=status.HTTP_200_OK)
        else:
            error_message = ", ".join([error for error in serializer.errors.keys()])
            error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class InterviewListView(ListAPIView):
    """
        List Api View: Api will give List of availble mock interview List and Upcoming Interviews
        Resposne: {
            "mocks": [
                {
                    "job_title": "Djangyghkjo Developer",
                    "company": "",
                    "exp_years": "",
                    "slug": ghvfw5lvb
                },
                {
                    "job_title": "Python developer",
                    "company": "",
                    "exp_years": "",
                    "slug": uvfw8lvg
                }
            ],
            "upcoming_interviews": [
                {
                    "date": "2020-08-21",
                    "job_title": "Byjus",
                    "slug": "rvfw5lvb"
                },
                {
                    "date": "2020-08-21",
                    "job_title": "Byjus",
                    "slug": "ip3fjjmo"
                }
            ]
        }
    """
    queryset = Interview.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        mock_list = []
        search_list = []
        if 'keyword' in request.GET.keys():
            keyword = request.GET.get('keyword')
            open_mocks = queryset.filter(Q(job_title__icontains=keyword) | Q(exp_years__icontains=keyword) |
                                         Q(skills__title__iexact=keyword)).distinct()

            for data in open_mocks:
                profile_obj = InterviewerProfile.objects.filter(user=data.interviewer).first()
                search_list.append({"job_title": data.job_title,
                                  "company": profile_obj.company if profile_obj else '',
                                  "exp_years": profile_obj.exp_years if profile_obj else '',
                                  "slug": data.slug
                                  })
        for data in queryset:
            profile_obj = InterviewerProfile.objects.filter(user=data.interviewer).first()
            mock_list.append({"job_title": data.job_title,
                              "company": profile_obj.company if profile_obj else '',
                              "exp_years": profile_obj.exp_years if profile_obj else '',
                              "slug": data.slug
                              })
        custom_booking_obj = BookInterview.objects.filter(is_payment_done=True)
        booking_list = []
        for each_row in custom_booking_obj:
            booking_list.append(
                {"date": each_row.date, "job_title": each_row.applied_designation, "slug": each_row.slug})

        response = {"mocks": mock_list, "upcoming_  interviews": booking_list, "search_list": search_list}
        return Response(response, status=status.HTTP_200_OK)