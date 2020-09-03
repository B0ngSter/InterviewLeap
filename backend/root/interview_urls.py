from django.urls import path
from authentication.views import InterviewCreateView, InterviewAcceptDeclineView, InterviewerRequestsListView

urlpatterns = [
    path('create-interview/', InterviewCreateView.as_view()),
    path('interview-requests/', InterviewerRequestsListView.as_view()),
    path('<str:slug>/<str:action>/', InterviewAcceptDeclineView.as_view()),
]
