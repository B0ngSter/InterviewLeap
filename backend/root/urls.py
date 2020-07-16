from django.urls import path
from .views import BookInterviewView

urlpatterns = [
    path('book-interview/', BookInterviewView.as_view())
]