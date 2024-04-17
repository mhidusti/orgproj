from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

class ServicesView(GenericAPIView):

    serializer_class = ServicesSerializer

    def get_queryset(self):
        services = Services.objects.filter(status=True)
        return services

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)


        return Response(
            serializer.data, status=status.HTTP_200_OK
        
        )