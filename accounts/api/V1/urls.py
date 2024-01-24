from django.urls import path, include
from .views import *
from rest_framework.authtoken.views import ObtainAuthToken


app_name = 'api-v1-accounts'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name = 'registration'),
    path('token/login/', ObtainAuthToken.as_view(), name = 'login'),
]
