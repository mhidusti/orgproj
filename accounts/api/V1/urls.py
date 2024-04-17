from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


app_name = "api-v1-accounts"

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("token/login/", CustomeObtainAuthToken.as_view(), name="login"),
    path("token/logout/", DestroyAuthToken.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/", ProfileView.as_view(), name="profile"),
    # path('verification/', VerificationView.as_view(), name = 'verification'),
    path("is-verified/<str:token>", IsVerifiedView.as_view(), name="is-verification"),
    path("resend/", ResendEmailView.as_view(), name="resend"),
    # jwt token
    path("token/create/", Customejwtview.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
