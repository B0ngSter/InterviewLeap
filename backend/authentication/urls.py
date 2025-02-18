from django.urls import path, include
from django_rest_passwordreset.views import reset_password_validate_token,\
    reset_password_request_token
from .views import LoginView, GoogleView, SignupView, CandidateProfileCreateListView, \
    InterviewerProfileCreateListView, CandidateProfileDetailView, InterviewerProfileDetailView, \
    IndustryListView, ResetPasswordConfirm, InterviewCreateView, VerifyUserView, basic_profile_details, \
    ResendEmailVerificationAPIView, InterviewAcceptDeclineView, InterviewerRequestsListView

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', basic_profile_details),
    path('google-signin', GoogleView.as_view()),
    path('resend-email/', ResendEmailVerificationAPIView.as_view()),
    path('password-reset/', reset_password_request_token, name='reset-password-request'),
    path('password-reset/validate_token/', reset_password_validate_token, name='reset-password-validate'),
    path('password-reset/confirm/', ResetPasswordConfirm.as_view(), name='reset-password-confirm'),
    path('candidate-profile/', CandidateProfileCreateListView.as_view()),
    path('interviewer-profile/', InterviewerProfileCreateListView.as_view()),
    # path('create-interview/', InterviewCreateView.as_view()),
    # path('interview-requests/', InterviewerRequestsListView.as_view()),
    path('interview/<str:slug>/<str:action>/', InterviewAcceptDeclineView.as_view()),
    path('verify-user/<str:token>', VerifyUserView.as_view()),
    # path('candidate-profile/<int:pk>/', CandidateProfileDetailView.as_view()),
    # path('interviewer-profile/<int:pk>/', InterviewerProfileDetailView.as_view())
]
