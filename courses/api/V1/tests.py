import pytest
from rest_framework.test import APIClient
from accounts.models import CustomeUser


@pytest.fixture
def client_api():
    client = APIClient()
    return client

@pytest.fixture
def user_test():
    user = CustomeUser.objects.create_user(username='test', password='H@midreza62', email='test@test.com')
    return user



@pytest.mark.django_db
class TestCourses:

    def test_view_api_course_list_view(self, client_api):
        url = "http://127.0.0.1:8000/courses/api/V1/courses/"
        response = client_api.get(url)
        assert response.status_code == 200

    def test_view_api_view_category(self):
        url = "http://127.0.0.1:8000/courses/api/V1/category/"
        client = APIClient()
        response = client.get(url)
        assert response.status_code == 200
        
    def test_view_api_create_category(self):
        url = "http://127.0.0.1:8000/courses/api/V1/category/"
        client = APIClient()
        data = {
            'name': 'test',
        }
        response = client.post(url, data=data)
        assert response.status_code == 401

    def test_view_api_create_category_with_normal_user(self, user_test):
        user = user_test
        url = "http://127.0.0.1:8000/courses/api/V1/category/"
        client = APIClient()
        client.force_authenticate(user)
        data = {
            'name': 'test',
        }
        response = client.post(url, data)
        assert response.status_code == 403

    def test_view_api_create_category_with_superuser(self ,user_test):
        user = user_test
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        url = "http://127.0.0.1:8000/courses/api/V1/category/"
        client = APIClient()
        client.force_authenticate(user)
        data = {
            'name': 'test',
        }
        response = client.post(url, data)
        assert response.status_code == 201


