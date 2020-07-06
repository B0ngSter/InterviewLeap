from django.urls import path, include
from .views import MyTokenObtainPairView, GoogleView, SignupView

urlpatterns = [
    # path('api/', include('djoser.urls')),
    # path('token/', include('djoser.urls.jwt')),
    path('signup', SignupView.as_view()),
    path('login', MyTokenObtainPairView.as_view()),
    path('google-signin', GoogleView.as_view())
]
