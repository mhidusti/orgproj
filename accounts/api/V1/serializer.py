from ...models import CustomeUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


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