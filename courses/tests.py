from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import *
from accounts.models import CustomeUser




class TestUrlCourse(TestCase):
     
    def test_view_courselist(self):
        url = reverse('courses:courses')
        self.assertEquals(resolve(url).func.view_class, CourseListView)

    def test_view_course_detail(self):
        url = reverse('courses:course_detail', kwargs={'pk':1})
        self.assertEquals(resolve(url).func.view_class, CourseDetailView)

    def test_view_course_cat(self):
        url = reverse('courses:course_cat', kwargs={'cat': 'test'})
        self.assertEquals(resolve(url).func.view_class, CourseListView)

    def test_view_course_delete(self):
        url = reverse('courses:delete', kwargs={'pk':1})
        self.assertEquals(resolve(url).func.view_class, DeleteCommentView)

    def test_view_payment_without_login(self):
        c = Client()
        url = reverse('courses:cart')
        respone = c.get(url)
        self.assertEqual(respone.status_code, 302)

    def test_view_payment_with_login(self):
        c = Client()
        user = CustomeUser.objects.create_user(email='user@user.com', username='user', password='passworD@123')
        url = reverse('courses:cart')
        c.force_login(user)
        respone = c.get(url)
        self.assertEqual(respone.status_code, 200)

        