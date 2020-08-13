from django.urls import path
from .views import BookInterviewView, TimeSlotListView, SkillSearchView, mojo_handler, CandidateInterviewerDashboardView

urlpatterns = [
    path('book-interview/', BookInterviewView.as_view()),
    path('time-slot/', TimeSlotListView.as_view()),
    path('skill-search', SkillSearchView.as_view()),
    path('dashboard/', CandidateInterviewerDashboardView.as_view()),
    path('webhook/payment-response/', mojo_handler)
]