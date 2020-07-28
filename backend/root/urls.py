from django.urls import path
from .views import BookInterviewView, TimeSlotListView

urlpatterns = [
    path('book-interview/', BookInterviewView.as_view()),
    path('time-slot/', TimeSlotListView.as_view())
]