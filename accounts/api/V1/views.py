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



class RegistrationView(GenericAPIView):
    
    serializer_class = RegisterationSerializer
    
    def post(self, request, *args, **kwargs):

        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print (serializer.validated_data)
            data = {
                'email': serializer.validated_data['email']
            }
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomeObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomeAuthTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
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

        return Response(data= {'detail':'password change successfully.', 'token':token.key}, status=status.HTTP_200_OK)
    

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
    

class VerificationView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        message=EmailMessage('email/email.html', "admin@test.ir",to=["test@test.com"])
        # message.send()
        email = SendEmailWithThreading(message)
        email.start()
        return Response({"detail" : "email sent for your verification...!"})