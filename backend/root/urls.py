from django.urls import path
from .views import BookInterviewView, TimeSlotListView, SkillSearchView, mojo_handler, CandidateDashboardView, MockBookingView, mock_booking_webhook_handler,\
    InterviewListView, CustomBookInterviewUpdateView, PastInterviewListView, ReportDetailView

urlpatterns = [
    path('book-interview/', BookInterviewView.as_view()),
    path('time-slot/', TimeSlotListView.as_view()),
    path('skill-search', SkillSearchView.as_view()),
    path('dashboard/', CandidateDashboardView.as_view()),
    path('interview-list/', InterviewListView.as_view()),
    path('past-interview/', PastInterviewListView.as_view()),
    path('webhook/payment-response/', mojo_handler, name='custom_booking'),
    path('book-mock/<slug:slug>/', MockBookingView.as_view()),
    path('webhook/mock-interview/', mock_booking_webhook_handler),
    path('book-interview/<slug:slug>/update/', CustomBookInterviewUpdateView.as_view()),
    path('report-details/<int:pk>/<slug:slug>/', ReportDetailView.as_view()),
]