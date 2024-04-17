from django.urls import path, include
from .views import *



app_name = 'root'

urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    path("test/",HomeView2.as_view(),name="home2"),

    path("about",about,name="about"),
    path("contact",contact,name="contact"),
    path("trainer",trainer,name="trainer"),
    path("api/V1/", include("root.api.V1.urls"))
]
