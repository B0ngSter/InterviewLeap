from django.urls import path
from authentication.views import InterviewCreateView, InterviewAcceptDeclineView, InterviewerRequestsListView

urlpatterns = [
    path('interview/create-interview/', InterviewCreateView.as_view()),
    path('interview/interview-requests/', InterviewerRequestsListView.as_view()),
    path('interview/<str:slug>/<str:action>/', InterviewAcceptDeclineView.as_view()),
]
