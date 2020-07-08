from django.urls import path, include
from .views import MyTokenObtainPairView, GoogleView, SignupView, CandidateProfileCreateListView, InterviewerProfileCreateListView, \
    CandidateProfileDetailView, InterviewerProfileDetailView

urlpatterns = [
    # path('api/', include('djoser.urls')),
    # path('token/', include('djoser.urls.jwt')),
    path('signup', SignupView.as_view()),
    path('login', MyTokenObtainPairView.as_view()),
    path('google-signin', GoogleView.as_view()),
    path('candidate-profile/', CandidateProfileCreateListView.as_view()),
    path('interviewer-profile/', InterviewerProfileCreateListView.as_view()),
    path('candidate-profile/<int:pk>/', CandidateProfileDetailView.as_view()),
    path('interviewer-profile/<int:pk>/', InterviewerProfileDetailView.as_view())
]
