
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializer import *
from ...models import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import viewsets
from .permission import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginator import CustomePaginate




# @api_view(["GET", "POST"])
# @permission_classes([IsAdminUser])
# def course_api_view(request):
#     if request.method == 'GET':
#         courses = Course.objects.filter(status=True)
#         courses_serilize = CourseSerializer(courses, many=True)
#         return Response(courses_serilize.data)
#     elif request.method == "POST":
#         course_serilize = CourseDetailSerializer(data=request.data)
#         if course_serilize.is_valid():
#             course_serilize.save()
#             return Response(course_serilize.data)
#         else:
#             return Response(course_serilize.errors)
        





# @api_view(["GET", "PUT", "DELETE"])
# def course_api_detail_view(request, pk):
#     course = get_object_or_404(Course, id=pk)
#     if request.method == "GET":
#         course_serilize = CourseDetailSerializer(course)
#         return Response(course_serilize.data)
#     elif request.method == "PUT":
#         course_serilize = CourseDetailSerializer(course, data=request.data)
#         course_serilize.is_valid(raise_exception=True)
#         course_serilize.save()
#         return Response(course_serilize.data)
#     elif request.method == "DELETE":
#         course.delete()
#         return Response("course deleted", status=status.HTTP_204_NO_CONTENT)




# class CourseListView(APIView):
#     #permission_classes = [IsAdminUser]
#     serializer_class = CourseSerializer

#     def get(self, request, *args, **kwargs):
#         courses = Course.objects.filter(status=True)
#         courses_serilize = CourseSerializer(courses, many=True)
#         return Response(courses_serilize.data)
#     def post(self, request, *args, **kwargs):
#         course_serilize = CourseSerializer(data=request.data)
#         if course_serilize.is_valid():
#             course_serilize.save()
#             return Response(course_serilize.data)
#         else:
#             return Response(course_serilize.errors)
        

# class CourseDetailView(APIView):
        
#     def get(self, request, *args, **kwargs):
#         course = get_object_or_404(Course, id=kwargs['pk'])
#         course_serilize = CourseDetailSerializer(course)
#         return Response(course_serilize.data)
    
#     def put(self, request, *args, **kwargs):
#         course = get_object_or_404(Course, id=kwargs['pk'])
#         course_serilize = CourseDetailSerializer(course, data=request.data)
#         course_serilize.is_valid(raise_exception=True)
#         course_serilize.save()
#         return Response(course_serilize.data)

#     def delete(self, request, *args, **kwargs):
#         course = get_object_or_404(Course, id=kwargs['pk'])
#         course.delete()
#         return Response("course deleted", status=status.HTTP_204_NO_CONTENT)


# class CourseDetailView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin):   
#     #queryset = Course.objects.filter(status=True)
#     serializer_class = CourseSerializer

#     def get_queryset(self):
#         return Course.objects.filter(status=True)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    

# class CourseListView(GenericAPIView, ListModelMixin, CreateModelMixin):   
#     #queryset = Course.objects.filter(status=True)
#     serializer_class = CourseSerializer

#     def get_queryset(self):
#         return Course.objects.filter(status=True)

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    

# class CourseDetailView:
#     pass

# class CourseListView(ListCreateAPIView):
#     queryset = Course.objects.filter(status=True)
#     serializer_class = CourseSerializer


# class CourseDetailView(UpdateAPIView, DestroyAPIView, RetrieveAPIView):   
#     queryset = Course.objects.filter(status=True)
#     serializer_class = CourseSerializer


# class CourseView(viewsets.ViewSet):
#     serializer_class = CourseSerializer
#     queryset = Course.objects.filter(status=True)

#     def list(self, request, *args, **kwargs):
#         courses_serializer = self.serializer_class(self.queryset, many=True)
#         return Response(courses_serializer.data)
    
#     def retrieve(self, request, *args, **kwargs):
#         course = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
#         courses_serializer = self.serializer_class(course)
#         return Response(courses_serializer.data)
        
#     def create(self, request, *args, **kwargs):
#          courses_serializer = self.serializer_class(data=request.data)
#          courses_serializer.is_valid(raise_exception=True)
#          courses_serializer.save()
#          return Response(courses_serializer.data)
    
#     def destroy(self, request, *args, **kwargs):
#         course = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
#         course.delete()
#         return Response("course deleted successfully")
    
#     def update(self, request, *args, **kwargs):
#         course = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
#         course_serializer = self.serializer_class(course, data=request.data)
#         course_serializer.is_valid(raise_exception=True)
#         course_serializer.save()
#         return Response(course_serializer.data)

class CourseView(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = CourseSerializer
    queryset = Course.objects.filter(status=True)
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['category', 'title']
    search_fields = ['content', 'category__name', 'teacher__info__email']
    ordering_fields = ['created_date']
    pagination_class = CustomePaginate



class CategoryView(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SkillsView(viewsets.ModelViewSet):
    serializer_class = SkillsSerializer
    queryset = Skills.objects.all()


class TrainerView(viewsets.ModelViewSet):
    serializer_class = TrainerSerializer
    queryset = Trainer.objects.filter(status=True)

