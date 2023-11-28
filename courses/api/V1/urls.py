from django.urls import path, include
from .views import *


app_name = 'api-v1'

urlpatterns = [
    path("courses/",course_api_view,name='courses'),
    path("course-detail/<int:pk>",course_api_detail_view,name='course-detail'),

]
