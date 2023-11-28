
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import CourseSerializer, CourseDetailSerializer
from ...models import Course
from django.shortcuts import get_object_or_404
from rest_framework import status



@api_view()
def course_api_view(request):
    courses = Course.objects.filter(status=True)
    courses_serilize = CourseSerializer(courses, many=True)
    return Response(courses_serilize.data)

@api_view(["GET", "POST", "PUT", "DELETE"])
def course_api_detail_view(request, pk):
    course = get_object_or_404(Course, id=pk)
    if request.method == "GET":
        course_serilize = CourseDetailSerializer(course)
        return Response(course_serilize.data)
    elif request.method == "POST":
        course_serilize = CourseDetailSerializer(data=request.data)
        if course_serilize.is_valid():
            course_serilize.save()
            return Response(course_serilize.data)
        else:
            return Response(course_serilize.errors)
    elif request.method == "PUT":
        course_serilize = CourseDetailSerializer(course, data=request.data)
        course_serilize.is_valid(raise_exception=True)
        course_serilize.save()
        return Response(course_serilize.data)
    elif request.method == "DELETE":
        course.delete()
        return Response("course deleted", status=status.HTTP_204_NO_CONTENT)
