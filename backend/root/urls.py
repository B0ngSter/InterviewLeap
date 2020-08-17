from django.urls import path
from .views import BookInterviewView, TimeSlotListView, SkillSearchView, mojo_handler, \
    CandidateInterviewerDashboardView, CandidateInterviewFeedbackView

urlpatterns = [
    path('book-interview/', BookInterviewView.as_view()),
    path('time-slot/', TimeSlotListView.as_view()),
    path('skill-search', SkillSearchView.as_view()),
    path('dashboard/', CandidateInterviewerDashboardView.as_view()),
    path('<slug:slug>/feedback/', CandidateInterviewFeedbackView.as_view()),
    path('webhook/payment-response/', mojo_handler)
]