import jwt
import pytz
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.dispatch import receiver
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django_rest_passwordreset.models import get_password_reset_token_expiry_time, ResetPasswordToken
from django_rest_passwordreset.serializers import PasswordTokenSerializer
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.utils.translation import ugettext as _
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView, \
    GenericAPIView, get_object_or_404
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from rest_framework_simplejwt.views import TokenObtainPairView
import tempfile
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from templated_mail.mail import BaseEmailMessage
from django.core import files
from django.db.models import Func
from django.db import models
from collections import OrderedDict

from root.models import BookInterview
from authentication.dates import by_month
from .interview_schedule import interview_schedule
from .serializers import RegistrationSerializer, VerifyUserSerializer, UserProfileSerializer, UserDetailSerializer, \
    ResendVerificationTokenSerializer, InterviewerRequestsListSerializer, PastInterviewSerializer, \
    CustomInterviewSerializer, MockInterviewSerializer, CandidateFresherSerializer, CandidateExperienceSerializer
from .models import User, CandidateProfile, InterviewerProfile, Interview, InterviewSlots
from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import AllowAny
# Create your views here.
from .serializers import CandidateProfileCreateListSerializer, InterviewerProfileCreateListSerializer, \
    CandidateProfileDetailSerializer, InterviewerProfileDetailSerializer, InterviewCreateSerializer


def generate_token(user):
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    return token


class SignupView(CreateAPIView):
    """
        create   -- Any user can Signup!
        actions -- send mail to the mentioned email id.
        Request params -- {
                              "email": "string",
                              "password": "string",
                              "confirm_password": "string",
                              "first_name": "string",
                              "last_name": "string",
                              "role": "string"
                            }
        Response Status -- 201 Ok
        Error Code -- 400 Bad Request

    """

    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            user = User.objects.get(email=serializer.data['email'])
            token = generate_token(user)
            self.account_email_verify_token(request, token, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if serializer.errors.get('message'):
                error_message = serializer.errors.get('message')[0]
            else:
                error_message = ", ".join([error.replace('_', ' ') for error in serializer.errors.keys()])
                error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def account_email_verify_token(self, request, token, data):
        try:
            email = data.get('email')
            first_name = data.get('first_name')
            role = data.get('role')
            frontend_url = settings.FRONTEND_URL
            send_by = settings.DEFAULT_FROM_EMAIL

            verification_url = "{frontend_url}/verify?token={token}".format(frontend_url=frontend_url,
                                                                                 token=str(token))
            print(verification_url)
            context = {
                'name': first_name,
                'site_name': 'Interview Leap',
                'verification_url': verification_url,
                'email': email
            }
            if role == 'Candidate':
                email_plaintext_message = render_to_string('email/verify_candidate.html', context)
            else:
                email_plaintext_message = render_to_string('email/verify_Interviewer.html', context)

            msg = EmailMultiAlternatives(
                "Welcome to {title}".format(title="Interview Leap!"),
                "",
                send_by,
                [email]
            )
            msg.attach_alternative(email_plaintext_message, 'text/html')
            msg.send()
        except BadHeaderError:
            message = "Invalid header found."
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


# class ConfirmationEmail(BaseEmailMessage):
#     template_name = "email/confirmation_email.html"
#
#     def get_context_data(self, **kwargs):
#         frontend_url = settings.FRONTEND_URL
#         user = User.objects.get(email=self.context['user'])
#         token = generate_token(user)
#
#         # This link will give profile completion link for user
#         verification_url = "{frontend_url}/auth/verify?token={token}".format(frontend_url=frontend_url,
#                                                                              token=str(token))
#         print(verification_url)
#         self.context = {
#             'name': user.first_name,
#             'site_name': 'Interview Leap',
#             'verification_url': verification_url
#         }
#         return self.context


class LoginView(TokenObtainPairView):
    """
        Login   -- Authenticated user will login!
        actions -- login
        Request params -- {
                              "email": "string",
                              "password": "string"
                            }
        Response Status -- 200 Ok along with tokens
        Error Code -- 400 Bad Request
        Error message -- Raise proper error messages

        """

    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        error_message = {}
        try:
            email = request.data["email"]
            password = request.data["password"]
            user = User.objects.filter(email=email).first()
            if not user:
                error_message['message'] = "User does not exist!"
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            elif not user.check_password(password):
                error_message['message'] = "Invalid password."
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            elif not user.role:
                error_message['message'] = "Role is not set for the User."
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            elif not user.email_verified:
                error_message['message'] = "Email is not verified."
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            error_message['message'] = "User does not exist!"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=email)
            is_profile_completed = False
            meta_data = {
                "meta_data": {"role": user.role, "full_name": user.get_full_name(),
                              "is_profile_completed": is_profile_completed}
            }
            try:
                candidate_profile = CandidateProfile.objects.get(user=user.id)
                if candidate_profile:
                    is_profile_completed = True
                    meta_data['meta_data']['is_profile_completed'] = is_profile_completed
                    if user.profile_picture:
                        meta_data['meta_data']['profile_picture'] = user.profile_picture.url
                else:
                    meta_data['meta_data']['profile_picture'] = None
            except ObjectDoesNotExist:
                interviewer_profile = InterviewerProfile.objects.filter(user=user.id).exists()
                if interviewer_profile:
                    is_profile_completed = True
                    meta_data['meta_data']['is_profile_completed'] = is_profile_completed
                    if user.profile_picture:
                        meta_data['meta_data']['profile_picture'] = user.profile_picture.url
                else:
                    meta_data['meta_data']['profile_picture'] = None

            response = serializer.validated_data
            response.update(meta_data)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResendEmailVerificationAPIView(APIView):
    """
        Resend request for email Verification  -- It send verification url link again to the requested Email Id!
        Request params -- {
                              "email": "string",
                            }
        Response Status -- 200 Ok
        Error Code -- 400 Bad Request
    """

    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = ResendVerificationTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data['email'])
            if user:
                token = generate_token(user)
                self.account_email_verify_token(request, token, user.email, user.first_name, user.role)
                message = "Email has been sent successfully to email {}".format(serializer.data['email'])
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User doest not exist!. Please signup first."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid request/Valid email is required"}, status=status.HTTP_400_BAD_REQUEST)

    def account_email_verify_token(self, request, token, email, first_name, role):
        try:
            frontend_url = settings.FRONTEND_URL
            send_by = settings.DEFAULT_FROM_EMAIL

            verification_url = "{frontend_url}/verify?token={token}".format(frontend_url=frontend_url,
                                                                                 token=str(token))
            context = {
                'name': first_name,
                'site_name': 'Interview Leap',
                'verification_url': verification_url,
                'email': email
            }
            if role == 'Candidate':
                email_plaintext_message = render_to_string('email/verify_candidate.html', context)
            else:
                email_plaintext_message = render_to_string('email/verify_Interviewer.html', context)

            msg = EmailMultiAlternatives(
                "Welcome to {title}".format(title="Interview Leap!"),
                "",
                send_by,
                [email]
            )
            msg.attach_alternative(email_plaintext_message, 'text/html')
            msg.send()
        except BadHeaderError:
            message = "Invalid header found."
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserView(RetrieveUpdateAPIView):
    """
        Action based on Verification token for email  -- If token is valid will verify the user and marked user as email_verified.
        Request param from GET call:     {
                              "token": "string",
                            }
        response : {
                    "is_token_valid": boolean
                    }
        Response Status -- 200 ok
        Error Code -- 400 Bad Request
    """

    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = VerifyUserSerializer

    def post(self, request, *args, **kwargs):
        token = kwargs.pop('token')
        payload = jwt.decode(token, settings.SECRET_KEY)
        response = {'is_token_valid': False}
        try:
            response['is_token_valid'] = User.objects.filter(id=payload.get('user_id'), email_verified=False).exists()
        except jwt.ExpiredSignature:
            response['message'] = 'Token expired. Please request for a new token'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidSignatureError:
            response['message'] = 'Signature verification failed'
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            response['message'] = 'Invalid Token'
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except jwt.InvalidTokenError:
            response['is_token_valid'] = User.objects.filter(id=payload.get('user_id'), email_verified=False).exists()
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_obj = get_object_or_404(User, id=payload.get('user_id'))
        serializer = self.serializer_class(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GoogleView(APIView):
    """
        Google Signup   -- An user can sign in using their google account like xyz@gmail.com!
                            Api will create a entry in user table passing Email id and password(auto-generated)
        Request Param - {"token": "string"}    #access_token
        status - "return token along with meta data"
        Error -- Raise with message error.
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        id_token = request.data['id_token']
        role = request.data.get('role')
        idinfo = requests.get("https://oauth2.googleapis.com/tokeninfo?id_token={}".format(id_token))
        data = json.loads(idinfo.text)

        if 'error' in data:
            content = {'message': 'Invalid token'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        response = {}
        try:
            user = User.objects.get(email=data.get('email'))
            if user.profile_picture:
                profile_picture = user.profile_picture.url
            else:
                profile_picture = None
            try:
                candidate_profile = CandidateProfile.objects.get(user=user.id)
                if candidate_profile:
                    is_profile_completed = True
                else:
                    is_profile_completed = False
            except ObjectDoesNotExist:
                try:
                    interviewer_profile = InterviewerProfile.objects.get(user=user.id)
                    if interviewer_profile:
                        is_profile_completed = True
                except ObjectDoesNotExist:
                    is_profile_completed = False
        except ObjectDoesNotExist:
            if not role:
                return Response(status=307)
            else:
                user = User()
                user.username = data['email']
                user.password = make_password(BaseUserManager().make_random_password())
                user.first_name = data.get('given_name')
                user.last_name = data.get('family_name')
                user.email = data['email']
                user.email_verified = True
                user.role = role

                if 'picture' in data.keys():
                    image_url = data.get('picture')
                    request = requests.get(image_url, stream=True)
                    file_name = image_url.split('/')[-1]
                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):  # Read the streamed image in sections
                        if not block:
                            break
                        lf.write(block)
                    user.profile_picture.save(file_name, files.File(lf))
                    profile_picture = user.profile_picture.url
                else:
                    profile_picture = None
                user.is_active = True
                user.save()
                is_profile_completed = False

        token = generate_token(user)
        response["access_token"] = token

        meta_data = \
            {
                "role": user.role,
                "full_name": user.get_full_name(),
                "profile_picture": profile_picture,
                "is_profile_completed": is_profile_completed,  # check profile and update this boolean
            }
        response.update({"meta_data": meta_data})
        return Response(response, status=status.HTTP_200_OK)


@csrf_protect
@api_view()
@permission_classes([AllowAny])
@authentication_classes([])
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        frontend_url = settings.FRONTEND_URL
        send_by = settings.DEFAULT_FROM_EMAIL
        host_link = "{frontend_url}/password-reset/".format(frontend_url=frontend_url)

        context = {
            'current_user': reset_password_token.user,
            'name': reset_password_token.user.first_name,
            'email': reset_password_token.user.email,
            'reset_password_url': host_link + "?token={token}".format(token=reset_password_token.key)

        }
        email_plaintext_message = render_to_string('email/reset_password.html', context)
        msg = EmailMultiAlternatives(
            "Password Reset for {title}".format(title="Interview Leap"),
            "",
            send_by,
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_plaintext_message, 'text/html')
        msg.send()
    except BadHeaderError:
        message = "Invalid header found."
        return Response({message: message}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirm(GenericAPIView):
    """
        An Api View which provides a method to reset a password based on a unique token
        Request params -- {
                          "token": "string",
                          "password": "string",
                        }
        Response Status --  {status: OK}
        Error Code -- 400 Bad Request
        Raise error with message

    """
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = ()
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']
        password_reset_token_validation_time = get_password_reset_token_expiry_time()
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()
        if reset_password_token is None:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)
        if timezone.now() > expiry_date:
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
        if reset_password_token.user.eligible_for_reset():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
            try:
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                )
            except ValidationError as e:
                raise exceptions.ValidationError({
                    'message': " ,".join(e.messages)
                })
            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user)
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()
        return Response({'status': 'OK'})


class CandidateProfileCreateListView(ListCreateAPIView):
    """
            CandidateProfile   -- Authenticated user can create profile!
            actions -- POST -- Profile Creation/Updation(Candidate), If profile exists it updates the profile.
            description -- Based on the professional status send the values
            Request params -- {
                                  "professional_status": "choicefield" --> options = ["Experienced", "Fresher"]
                                  "education": "string",
                                  "college": "string"
                                  "years_of_passing": "string"
                                  "job_title": "string"
                                  "resume": "file field"
                                  "linkedin": "valid url in string"
                                  "industry": "string"
                                  "designation": "string"
                                  "company": "string"
                                  "exp_years": "integer"
                                  "skills": "comma separated values in string"

                                }
            Response Status -- 200 Ok along with candidateprofile details
            Error Code -- 400 Bad Request
            Error message -- Raise proper error messages

            """
    serializer_class = CandidateProfileCreateListSerializer

    def get(self, request, *args, **kwargs):

        if request.GET.get('email'):
            user = User.objects.get(email=request.GET.get('email'))
            candidate_user_info = UserDetailSerializer(user).data
            candidate = CandidateProfile.objects.get(user__email=request.GET.get('email'))
            if candidate.professional_status == 'Fresher':
                serialize = CandidateFresherSerializer(candidate).data
                serialize.update(candidate_user_info)
                return Response(serialize, status=status.HTTP_200_OK)
            else:
                serialize = CandidateExperienceSerializer(candidate).data
                serialize.update(candidate_user_info)
                return Response(serialize, status=status.HTTP_200_OK)

        candidate_serializer = {}
        user_serializer = UserDetailSerializer(self.request.user).data
        try:
            candidate_obj = CandidateProfile.objects.get(user=self.request.user)
            candidate_serializer = CandidateProfileCreateListSerializer(candidate_obj).data
            candidate_serializer.update(user_serializer)
        except ObjectDoesNotExist:
            candidate_serializer.update(user_serializer)
        return Response(candidate_serializer, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        profile_data = request.data.dict()
        profile_data['user'] = request.user.id
        try:
            candidate_obj = CandidateProfile.objects.get(user=self.request.user.id)
            if not request.data.get('resume', None) and candidate_obj.resume:
                profile_data['resume'] = candidate_obj.resume
        except ObjectDoesNotExist:
            pass
        user_serializer = UserProfileSerializer(request.user, data=profile_data, partial=True,
                                                context={"request": request})
        if user_serializer.is_valid():
            user_serializer.save()
        if 'skills' in profile_data:
            profile_data['skills'] = [{'title': skill} for skill in profile_data['skills'].split(",")]
        serializer = self.get_serializer(data=profile_data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            response.update(user_serializer.data)
            return Response(response, status=status.HTTP_200_OK)
        else:
            error_message = ", ".join([error for error in serializer.errors.keys()])
            error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class InterviewerProfileCreateListView(ListCreateAPIView):
    """
                InterviewerProfile   -- Authenticated user can create profile!
                actions -- POST -- Profile Creation/Updation(Interviewer), If profile exists it updates the profile.
                Request params -- {
                                      "industry": "string",
                                      "designation": "string"
                                      "company": "string"
                                      "exp_years": "integer"
                                      "resume": "file field"
                                      "linkedin": "valid url in string"
                                      "skills": "comma separated values in string"

                                    }
                Response Status -- 200 Ok along with interviewerprofile details
                Error Code -- 400 Bad Request
                Error message -- Raise proper error messages

                """
    serializer_class = InterviewerProfileCreateListSerializer

    def get(self, request, *args, **kwargs):
        interviewer_serializer = {}
        user_serializer = UserDetailSerializer(self.request.user).data
        try:
            interviewer_obj = InterviewerProfile.objects.get(user=self.request.user)
            interviewer_serializer = InterviewerProfileCreateListSerializer(interviewer_obj).data
            interviewer_serializer.update(user_serializer)
        except ObjectDoesNotExist:
            interviewer_serializer.update(user_serializer)
        return Response(interviewer_serializer, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        profile_data = request.data.dict()
        profile_data['user'] = request.user.id
        profile_data['account_info'] = json.loads(profile_data['account_info'])
        try:
            interviewer_obj = InterviewerProfile.objects.get(user=self.request.user.id)
            if not request.data.get('resume', None) and interviewer_obj.resume:
                profile_data['resume'] = interviewer_obj.resume
        except ObjectDoesNotExist:
            pass
        user_serializer = UserProfileSerializer(request.user, data=profile_data, partial=True,
                                                context={"request": request})
        if user_serializer.is_valid():
            user_serializer.save()
        if 'skills' in profile_data:
            profile_data['skills'] = [{'title': skill} for skill in profile_data['skills'].split(",")]
        serializer = self.get_serializer(data=profile_data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            response.update(user_serializer.data)
            return Response(response, status=status.HTTP_200_OK)
        else:
            if serializer.errors.get('message'):
                error_message = serializer.errors.get('message')[0]
            else:
                if 'account_info' in serializer.errors.keys():
                    error_message = "Please provide valid values for Account Details form"
                else:
                    error_message = ", ".join([error for error in serializer.errors.keys()])
                    error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class CandidateProfileDetailView(RetrieveUpdateAPIView):
    """
               CandidateProfile   -- Authenticated user can GET Candidate profile details!
               actions -- GET -- Profile Details(Candidate)
               Response params -- {
                                     "education": "string",
                                     "college": "string"
                                     "years_of_passing": "string"
                                     "job_title": "string"
                                     "resume": "file field"
                                     "linkedin": "valid url in string"
                                     "skills": "comma separated values in string"

                                   }
               Response Status -- 200 Ok along with candidateprofile details
               Error Code -- 400 Bad Request
               Error message -- Raise proper error messages

               """

    lookup_field = 'pk'
    serializer_class = CandidateProfileDetailSerializer

    def get_queryset(self):
        candidate = CandidateProfile.objects.all()
        return candidate

    def update(self, request, *args, **kwargs):
        profile_data = request.data.dict()
        candidate_obj = self.get_object()
        if 'skills' in profile_data:
            profile_data['skills'] = [{'title': skill} for skill in profile_data['skills'].split(",")]
        serializer = self.get_serializer(candidate_obj, data=profile_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = ", ".join([error for error in serializer.errors.keys()])
            error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class InterviewerProfileDetailView(RetrieveUpdateAPIView):
    """
    InterviewerProfile   -- Authenticated user can GET Interveiwer profile details!
    actions -- GET -- Profile Details(Interviewer)
    Response params -- {
        "industry": "string",
        "designation": "string"
        "company": "string"
        "exp_years": "integer"
        "resume": "file field"
        "linkedin": "valid url in string"
        "skills": "comma separated values in string"
    }
    Response Status -- 200 Ok along with interveiwerprofile details
    Error Code -- 400 Bad Request
    Error message -- Raise proper error messages
    """

    lookup_field = 'pk'
    serializer_class = InterviewerProfileDetailSerializer

    def get_queryset(self):
        interviewer = InterviewerProfile.objects.all()
        return interviewer

    def update(self, request, *args, **kwargs):
        profile_data = request.data.dict()
        interviewer_obj = self.get_object()
        if 'skills' in profile_data:
            profile_data['skills'] = [{'title': skill} for skill in profile_data['skills'].split(",")]
        serializer = self.get_serializer(interviewer_obj, data=profile_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = ", ".join([error for error in serializer.errors.keys()])
            error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class IndustryListView(APIView):
    """
       Retrieve -- Retrieve list of Industries.
       Actions -- GET method
       Response Status -- 200 Ok
    """

    def get(self, request, *args, **kwargs):
        industries = settings.INDUSTRY_CHOICES
        industries = [industry[0] for industry in industries]
        return Response({"industries": industries})


class InterviewCreateView(CreateAPIView):
    """
        InterviewCreationDetails   -- Authenticated Interviewer can Post Interveiw details!
        actions -- Post -- Interview Details(Interviewer)
        Request params -- {
                    "job_title": "software engineer", (string)
                    "exp_years": 2, (integer)
                    "date": "2020-06-21", (string)
                    "time_slots": [
                        {
                            "start_time": "10:00",
                            "end_time": "11:00"
                        },
                        {
                            "start_time": "11:00",
                            "end_time": "12:00"
                        }
                    ] (array with json field)
                }
        Response Status -- 200 Ok along with interveiwe details
        Error Code -- 400 Bad Request
        Error message -- Raise proper error messages
        """

    serializer_class = InterviewCreateSerializer

    def create(self, request, *args, **kwargs):
        interview_dict = request.data
        interview_dict['interviewer'] = request.user.id
        if 'skills' in interview_dict:
            interview_dict['skills'] = [{'title': skill} for skill in interview_dict['skills'].split(",")]
        serializer = self.get_serializer(data=interview_dict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = ", ".join([error for error in serializer.errors.keys()])
            error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class InterviewAcceptDeclineView(CreateAPIView):
    """
        InterviewAcceptDecline   -- Interviewer Side
        actions -- Post -- Interview Accept/Decline(Interviewer)
        api -- auth/interviewer/12/accept/  -- in accept place it can be (accept/decline)
        Request params -- {
                    "candidate_email": "madhu@gmail.com", (string)
                    "date": "2020-06-21", (string)
                    "start_time": "10:00",
                    "end_time": "11:00"
                    }

        Response Dict -- {
                    "message": "Interview Invite has been sent to Candidate Successfully",
                    "interview_link": "https://www.google.com/calendar/event?eid=djZlNTI1ODUyNGEyAc3RvY2tyb29tLmlv"
                    }
        Response Status -- 200 Ok along with interview link details and success message
        Error Code -- 400 Bad Request
        Error message -- Raise proper error messages
        """

    def _date_time_naive_format(self, date, time):
        date_time = date + ' ' + time
        naive = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        return naive

    def _date_time_format(self, date, time, timezone):
        date_time = date + ' ' + time
        local = pytz.timezone(timezone)
        naive = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc).isoformat()
        return utc_dt

    def create(self, request, *args, **kwargs):
        if self.kwargs['action'] == 'accept':
            interview_info = request.data.dict()
            interview_obj = Interview.objects.get(interviewer=self.request.user, pk=self.kwargs['pk'])
            interview_info["recipients"] = [request.data['candidate_email'], 'madhu@equiv.in']
            interview_info['start_time'] = self._date_time_naive_format(request.data['date'],
                                                                        request.data['start_time'])
            interview_info['end_time'] = self._date_time_naive_format(request.data['date'], request.data['end_time'])
            interview_slot = InterviewSlots.objects.get(interview=interview_obj,
                                                        interview_start_time=interview_info['start_time'],
                                                        interview_end_time=interview_info['end_time'])
            timezone = interview_obj.timezone
            interview_info['start_time'] = self._date_time_format(request.data['date'], request.data['start_time']
                                                                  , timezone)
            interview_info['end_time'] = self._date_time_format(request.data['date'], request.data['end_time']
                                                                , timezone)
            interview_info['timezone'] = interview_obj.timezone
            interview_info['title'] = interview_obj.job_title
            interview_info['description'] = interview_obj.description
            response = interview_schedule(interview_info)
            interview_link = response['htmlLink']
            candidate_obj = User.objects.get(email=request.data['candidate_email'])
            interview_slot.__dict__.update({'candidate': candidate_obj})
            interview_slot.save()
            success_message = "Interview Invite has been sent to Candidate Successfully"
            return Response({"message": success_message,
                             "interview_link": interview_link}, status=status.HTTP_200_OK)
        elif self.kwargs['action'] == 'decline':
            pass
        else:
            return Response({'message': "Not a valid action"}, status=status.HTTP_400_BAD_REQUEST)


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class InterviewerRequestsListView(ListCreateAPIView):
    """
           Retrieve -- Retrieve list of interview requests to Interviewer booked by candidate(custom interviews).
           Actions -- GET method
           Response Status -- 200 Ok
           Response sample dict -- {
                    "id": 1,
                    "booking_id": "RHHG75SD",
                    "company_type": null,
                    "applied_designation": null,
                    "date": null,
                    "time_zone": null,
                    "time_slots": [],
                    "is_payment_done": false,
                    "candidate": 14,
                    "payment_detail": null,
                    "skills": [
                        python,django
                    ]
                }
            ]
    """

    serializer_class = InterviewerRequestsListSerializer

    def _date_time_naive_format(self, date, time):
        date_time = date + ' ' + time
        naive = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        return naive

    def _date_time_format(self, date, time, timezone):
        date_time = date + ' ' + time
        local = pytz.timezone(timezone)
        naive = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc).isoformat()
        return utc_dt

    def get(self, request, *args, **kwargs):
        mock_interviews = InterviewSlots.objects.filter(interview__interviewer=self.request.user)
        custom_interviews = BookInterview.objects.filter(interviewer__user=self.request.user)
        mock_interviews_feedback = mock_interviews.filter(interview_start_time__lt=timezone.now(),
                                                          interview_end_time__lt=timezone.now(),
                                                          feedback__isnull=True).order_by('created_at')
        custom_interviews_feedback = custom_interviews.filter(interview_start_time__lt=timezone.now(),
                                                              interview_end_time__lt=timezone.now(),
                                                              feedback__isnull=True).order_by('created_at')
        allotted_mock_interviews = mock_interviews.filter(interview_start_time__gte=timezone.now(),
                                                          interview_end_time__gte=timezone.now(),
                                                          candidate__isnull=False)
        allotted_custom_interviews = custom_interviews.filter(interview_start_time__gte=timezone.now(),
                                                              interview_end_time__gte=timezone.now())
        serializer = {}
        try:
            skills = InterviewerProfile.objects.get(user=self.request.user).skills.values_list('title', flat=True)

            interview_requests = BookInterview.objects.filter(
                                                              is_interview_scheduled=False, interviewer__isnull=True,
                                                              is_declined=False)
            for skill in skills:
                interview_requests = interview_requests.filter(skills__title__icontains=skill)
            serializer['interview_requests'] = self.get_serializer(interview_requests, many=True).data
        except ObjectDoesNotExist:
            serializer['interview_requests'] = []

        serializer['custom_feedback'] = CustomInterviewSerializer(custom_interviews_feedback, many=True).data
        serializer['mock_feedback'] = MockInterviewSerializer(mock_interviews_feedback, many=True).data
        serializer['feedback'] = serializer.pop('custom_feedback') + serializer.pop('mock_feedback')
        serializer['allotted_custom_interviews'] = CustomInterviewSerializer(allotted_custom_interviews, many=True).data
        serializer['allotted_mock_interviews'] = MockInterviewSerializer(allotted_mock_interviews, many=True).data
        serializer['upcoming_interviews'] = serializer.pop('allotted_custom_interviews') + \
                                            serializer.pop('allotted_mock_interviews')
        past_mock_interviews = InterviewSlots.objects.filter(interview__interviewer=self.request.user,
                                                             interview_start_time__lt=timezone.now(),
                                                             interview_end_time__lt=timezone.now(),
                                                             feedback__isnull=False,
                                                             candidate__isnull=False)

        if past_mock_interviews:
            mock_interviews_month = list(by_month(past_mock_interviews, 'interview_start_time'))
        else:
            mock_interviews_month = []

        past_interviews = {}
        for months, values in mock_interviews_month:
            past_interview_serializer = PastInterviewSerializer(values, many=True).data
            past_interviews.update({months.strftime("%B"): past_interview_serializer})
        if not request.data.get('sort_by') == 'oldest':
            past_interviews = OrderedDict(reversed(list(past_interviews.items())))

        serializer['past_interviews'] = past_interviews
        return Response(serializer, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        interview_info = request.data
        if interview_info['action'] == 'accept':
            interview_obj = BookInterview.objects.get(candidate__email=request.data["candidate_email"],
                                                      slug=interview_info['slug'])
            if interview_obj.interviewer:
                return Response({"message": "Sorry this interview is already taken by other Interviewer"},
                                status=status.HTTP_400_BAD_REQUEST)
            timezone = interview_obj.time_zone
            interview_info["recipients"] = [request.data['candidate_email'], self.request.user.email]
            interview_info['start_time'] = self._date_time_format(request.data['date'], request.data['start_time']
                                                                  , timezone)
            interview_info['end_time'] = self._date_time_format(request.data['date'], request.data['end_time']
                                                                , timezone)
            interview_info['timezone'] = timezone
            interview_info['title'] = interview_obj.applied_designation
            interview_info['description'] = ""
            response = interview_schedule(interview_info)
            interview_link = response['htmlLink']
            interviewer = InterviewerProfile.objects.get(user=self.request.user)
            interview_obj.interviewer = interviewer
            interview_obj.meet_link = interview_link
            interview_obj.is_interview_scheduled = True
            interview_obj.interview_start_time = interview_info['start_time']
            interview_obj.interview_end_time = interview_info['end_time']
            interview_obj.save()
            success_message = "Interview Invite has been sent to Candidate Successfully"
            return Response({"message": success_message,
                             "interview_link": interview_link}, status=status.HTTP_200_OK)
        elif interview_info['action'] == 'decline':
            interview_obj = BookInterview.objects.get(candidate__email=request.data["candidate_email"],
                                                      slug=interview_info['slug'])
            interview_obj.is_declined = True
            interview_obj.save()
            return Response({"message": "Interview Declined"})
        else:
            return Response({'message': "Not a valid action"}, status=status.HTTP_400_BAD_REQUEST)


def basic_profile_details(request):
    if request.user.is_authenticated:
        payload = {'profile': {'first_name': request.user.first_name, 'last_name': request.user.last_name,
                               'role': request.user.role}}
        if request.user.profile_picture:
            payload['profile']['profile_picture'] = request.user.profile_picture.url
        return JsonResponse(payload, status=200)
    else:
        return JsonResponse({'profile': None, 'message': 'Login to continue'}, status=401)
