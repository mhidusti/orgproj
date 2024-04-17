from rest_framework.generics import GenericAPIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from .multi_threading import SendEmailWithThreading
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from .tasks import send_email_with_celery

class RegistrationView(GenericAPIView):
    """
    this class is for create user
    """

    serializer_class = RegisterationSerializer

    def post(self, request, *args, **kwargs):

        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                CustomeUser, email=serializer.validated_data["email"]
            )
            token = self.get_tokens_for_user(user)
            send_email_with_celery.delay("email/email.html", token, "admin@hamid.com", [user.email])
            
            
            

            return Response({"detail": "if email is on our database email sent for your verification...!"})

            # print (serializer.validated_data)
            # data = {
            #     'email': serializer.validated_data['email']
            # }
            # return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomeObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomeAuthTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class DestroyAuthToken(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Customejwtview(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer


class ChangePasswordView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.check_old_password(request, serializer.validated_data)
        serializer.set_new_password(request, serializer.validated_data)
        token = serializer.create_new_token(request, serializer.validated_data)

        return Response(
            data={"detail": "password change successfully.", "token": token.key},
            status=status.HTTP_200_OK,
        )


class ProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        serializer = self.serializer_class(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        serializer = self.serializer_class(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


# class VerificationView(GenericAPIView):

#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(CustomeUser, email = "admin@hamid.com")
#         token = self.get_tokens_for_user(user)
#         message = EmailMessage('email/email.html', {'user': 'hamid', "token":token}, 'admin@hamid.com', to=["admin@hamid.com"])
#         email = SendEmailWithThreading(message)
#         email.start()
#         return Response({"detail" : "email sent for your verification...!"})


#     def get_tokens_for_user(self, user):

#         refresh = RefreshToken.for_user(user)
#         return str(refresh.access_token)


class IsVerifiedView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            user_data = AccessToken(kwargs.get("token"))
            user_id = user_data["user_id"]
            user = get_object_or_404(CustomeUser, id=user_id)
            user.is_verified = True
            user.save()
            return Response({"detail": "your account verified successfully"})
        except:
            return Response(
                {
                    "detail": "your token may be expired or changed structure...",
                    "resend email": "http://127.0.0.1:8080/accounts/api/V1/resend",
                }
            )


class ResendEmailView(GenericAPIView):
    serializer_class = ResendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.is_verified:
            return Response({"detail": "your email is already verified"})
        token = self.get_tokens_for_user(user)
        message = EmailMessage(
            "email/email.html",
            {"token": token},
            "admin@hamid.com",
            to=[serializer.validated_data["email"]],
        )
        email = SendEmailWithThreading(message)
        email.start()
        return Response({"detail": "email Resend for you..."})

    def get_tokens_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
