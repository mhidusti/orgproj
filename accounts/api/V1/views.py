from rest_framework.generics import GenericAPIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status


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