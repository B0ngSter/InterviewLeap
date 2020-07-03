from django.urls import path, include
from .views import MyTokenObtainPairView, GoogleView

urlpatterns = [
    path('api/', include('djoser.urls')),
    path('token/', include('djoser.urls.jwt')),
    path('login', MyTokenObtainPairView.as_view()),
    path('google-signin', GoogleView.as_view())
]
