from ...models import CustomeUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegisterationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=20, write_only=True)
    
    class Meta:
        model = CustomeUser
        fields = ['email', 'username', 'password', 'password1']


    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password')

        if password1 != password2:
            raise serializers.ValidationError({
                'detail' : 'password dose not confirmed'
            })
        
        try:

            validate_password(password1)
        
        except exceptions.ValidationError as e:

            raise serializers.ValidationError({
                'detail' : list(e.messages)
            })
        

        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password1', None)
        return CustomeUser.objects.create_user(**validated_data)
    

class CustomeAuthTokenSerializer(serializers.Serializer):
        email = serializers.CharField(
        label=("Email"),
        write_only=True
    )
        password = serializers.CharField(
            label=("Password"),
            style={'input_type': 'password'},
            trim_whitespace=False,
            write_only=True
        )
        token = serializers.CharField(
            label=("Token"),
            read_only=True
        )

        def validate(self, attrs):
            email = attrs.get('email')
            password = attrs.get('password')

            if email and password:
                user = authenticate(request=self.context.get('request'),
                                    email=email, password=password)

                # The authenticate call simply returns None for is_active=False
                # users. (Assuming the default ModelBackend authentication
                # backend.)
                if not user:
                    msg = ('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg, code='authorization')
                if not user.is_verified:
                    msg = ('your account is not verified !...')
                    raise serializers.ValidationError(msg, code='authorization')
                     
            else:
                msg = ('Must include "email" and "password".')
                raise serializers.ValidationError(msg, code='authorization')
            attrs['user'] = user
            return attrs
        

class CustomObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self,attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            msg = ('your account is not verified !...')
            raise serializers.ValidationError(msg, code='authorization')
        validated_data['id'] = self.user.id
        validated_data['email'] = self.user.email
        return validated_data
        


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(max_length=20)
    new_password1 = serializers.CharField(max_length=20)
    new_password2 = serializers.CharField(max_length=20)


    def validate(self, attrs):
        pass1 = attrs.get('new_password1')
        pass2 = attrs.get('new_password2')

        if pass1 != pass2:
            raise serializers.ValidationError({
                'detail' : 'pass1 and pass2 must be the same'
            })
        
        return super().validate(attrs)
    

    def check_old_password(self, request, attrs:dict):

        old_pass = attrs.get('old_password')
        pass1 = attrs.get('new_password1')
        user = request.user
        if not user.check_password(old_pass):
                        raise serializers.ValidationError({
                'detail' : 'old_password is not confirmed'
            })
        
        if old_pass == pass1 :
             raise serializers.ValidationError({
                'detail' : 'old_password can not same as new pass'
            })
             
        
        return attrs
    

    def set_new_password(self, request, attrs:dict):
        pass1 = attrs.get('new_password1')
        user = request.user
        try:

            validate_password(pass1)
        
        except exceptions.ValidationError as e:

            raise serializers.ValidationError({
                'detail' : list(e.messages)
            })
        
        user.set_password(pass1)
        user.save()
        return attrs
    
    def create_new_token(self, request, attrs:dict):
         user = request.user

         try : 
              user.auth_token.delete()
              Token.objects.create(user=user)
         except :
              Token.objects.create(user=user)
         token = Token.objects.get(user=user)
         return  token
    
from ...models import Profile
class ProfileSerializer(serializers.ModelSerializer):
     email = serializers.CharField(max_length=100, source='user.email', read_only=True)
     
     class Meta:
          model = Profile
          fields = ['id', 'first_name', 'last_name', 'image', 'email']























        