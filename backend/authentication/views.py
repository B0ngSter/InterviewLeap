from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext as _
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from templated_mail.mail import BaseEmailMessage
from .models import User

# Create your views here.


def generate_token(user):
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    return token


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