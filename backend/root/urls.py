from django.urls import path
from .views import BookInterviewView, TimeSlotListView, SkillSearchView

urlpatterns = [
    path('book-interview/', BookInterviewView.as_view()),
    path('time-slot/', TimeSlotListView.as_view()),
    path('skill-search', SkillSearchView.as_view()),
]