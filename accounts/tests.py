from django.test import TestCase
from .forms import EditProfile
from .models import CustomeUser

# Create your tests here.

class TestAccount(TestCase):

    def setUp(self):
        self.user = CustomeUser.objects.create_user(email='test@test.com', username='test', password='H@midreza62')

    def test_form_edit_profile_false(self):
        
        data = {
            'user': 'ali',
            'first_name': 'hamid',
            'last_name': 'mehrabi',
            }
        form = EditProfile(data=data)
        self.assertFalse(form.is_valid())


    def test_form_edit_profile_true(self):

        data = {
            'user': self.user,
            'first_name': 'hamid',
            'last_name': 'mehrabi',
            }
        form = EditProfile(data=data)
        self.assertTrue(form.is_valid())


    def test_model_custome_user_model(self):
        self.assertEqual(self.user.email,'test@test.com' )

    def test_model_custome_user_model_2(self):
        
        self.assertTrue(CustomeUser.objects.filter(id=self.user.id).exists())