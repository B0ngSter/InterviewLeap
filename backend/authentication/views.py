from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.utils.translation import ugettext as _
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from rest_framework_simplejwt.views import TokenObtainPairView
import tempfile
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from templated_mail.mail import BaseEmailMessage
from django.core import files
from .serializers import RegistrationSerializer
from .models import User, CandidateProfile, InterviewerProfile

# Create your views here.
from .serializers import CandidateProfileCreateListSerializer, InterviewerProfileCreateListSerializer, \
    CandidateProfileDetailSerializer, InterviewerProfileDetailSerializer


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
                              "re_password": "string",
                              "first_name": "string",
                              "last_name": "string",
                              "role": "string"
                            }
        Response Status -- 201 Ok
        Error Code -- 400 Bad Request

    """

    permission_classes = (AllowAny,)
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
                error_message = ", ".join([error for error in serializer.errors.keys()])
                error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def account_email_verify_token(self, request, token, data):
        try:
            email = data.get('email')
            first_name = data.get('first_name')
            frontend_url = settings.FRONTEND_URL
            send_by = settings.DEFAULT_FROM_EMAIL

            verification_url = "{frontend_url}/auth/verify?token={token}".format(frontend_url=frontend_url,
                                                                                 token=str(token))
            print(verification_url)
            context = {
                'name': first_name,
                'site_name': 'Interview Leap',
                'verification_url': verification_url,
                'email': email
            }

            email_plaintext_message = render_to_string('confirmation_email.html', context)
            msg = EmailMultiAlternatives(
                "Welcome to {title}".format(title="Interview Leap!"),
                "",
                send_by,
                [email]
            )
            msg.attach_alternative(email_plaintext_message, 'text/html')
            msg.send()
        except:
            raise exceptions.ValidationError


class ConfirmationEmail(BaseEmailMessage):
    template_name = "confirmation_email.html"

    def get_context_data(self, **kwargs):
        frontend_url = settings.FRONTEND_URL
        user = User.objects.get(email=self.context['user'])
        token = generate_token(user)

        # This link will give profile completion link for user
        verification_url = "{frontend_url}/auth/verify?token={token}".format(frontend_url=frontend_url,
                                                                             token=str(token))
        print(verification_url)
        self.context = {
            'name': user.first_name,
            'site_name': 'Interview Leap',
            'verification_url': verification_url
        }
        return self.context


class MyTokenObtainPairView(TokenObtainPairView):
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

        except ObjectDoesNotExist:
            error_message['message'] = "User does not exist!"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=email)
            is_profile_completed = False
            meta_data = {
                "meta_data": {"role": user.role, "full_name": user.get_full_name(), "is_profile_completed": is_profile_completed}
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


class GoogleView(APIView):
    """
        Google Signup   -- An user can sign in using their google account like xyz@gmail.com!
                            Api will create a entry in user table passing Email id and password(auto-generated)
        Request Param - {"token": "string"}    #access_token
        status - "return verification token"
        Error -- Raise with message error.
    """
    permission_classes = (AllowAny,)

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
                candidate_profile = CandidateProfile.objects.get(user=user.id).exists()
                if candidate_profile:
                    token = RefreshToken.for_user(user)  # generate token manually without username & password
                    response['access_token'] = str(token.access_token)
                    is_profile_completed = True
                else:
                    token = generate_token(user)
                    response["verification_token"] = token
                    is_profile_completed = False

            except ObjectDoesNotExist:
                interviewer_profile = InterviewerProfile.objects.get(user=user.id).exists()
                if interviewer_profile:
                    token = RefreshToken.for_user(user)  # generate token manually without username & password
                    response['access_token'] = str(token.access_token)
                    is_profile_completed = True
                else:
                    token = generate_token(user)
                    response["verification_token"] = token
                    is_profile_completed = False
        except ObjectDoesNotExist:
            user = User()
            user.username = data['email']
            user.password = make_password(BaseUserManager().make_random_password())
            user.first_name = data.get('given_name')
            user.last_name = data.get('family_name')
            user.email = data['email']
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
            response["verification_token"] = token

        meta_data = \
            {
                "role": user.role,
                "full_name": user.get_full_name(),
                "profile_picture": profile_picture,
                "is_profile_completed": is_profile_completed,          # check profile and update this boolean
            }
        response.update({"meta_data": meta_data})
        return Response(response, status=status.HTTP_200_OK)


class CandidateProfileCreateListView(ListCreateAPIView):
    """
            CandidateProfile   -- Authenticated user can create profile!
            actions -- POST -- Profile Creation/Updation(Candidate), If profile exists it updates the profile.
            Request params -- {
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
    serializer_class = CandidateProfileCreateListSerializer

    def get_queryset(self):
        candidates = CandidateProfile.objects.all()
        return candidates

    def create(self, request, *args, **kwargs):
        profile_data = request.data.dict()
        profile_data['user'] = request.user.id
        profile_data['skills'] = [{'title': skill} for skill in profile_data['skills'].split(",")]
        serializer = self.get_serializer(data=profile_data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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

    def get_queryset(self):
        interviewers = InterviewerProfile.objects.all()
        return interviewers

    def create(self, request, *args, **kwargs):
        profile_data = request.data.dict()
        profile_data['user'] = request.user.id
        profile_data['skills'] = [{'title': skill} for skill in profile_data['skills'].split(",")]
        serializer = self.get_serializer(data=profile_data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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

