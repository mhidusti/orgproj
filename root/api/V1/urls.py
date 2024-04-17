from django.urls import path, include
from .views import *


app_name = "api-v1-root"

urlpatterns = [
    path("services/", ServicesView.as_view(), name="api-services"),
]