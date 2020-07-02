from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('token/', include('djoser.urls.jwt')),
]
