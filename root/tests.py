from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import *
from .forms import *


# Create your tests here.


class TestUrlRoot(TestCase):
    def setUp(self):
        self.url1 = reverse('root:home')
        self.url2 = reverse('root:contact')
        self.url3 = reverse('root:about')
        self.url4 = reverse('root:trainer')
     
    def test_view_home(self):
        self.assertEquals(resolve(self.url1).func.view_class, HomeView)

    def test_view_contact(self):
        self.assertEquals(resolve(self.url2).func, contact)


    def test_view_about(self):
        self.assertEquals(resolve(self.url3).func, about)

    
    def test_view_trainer(self):  
        self.assertEquals(resolve(self.url4).func, trainer)

    def test_form_newsletter(self):
        form = NewsLetterForm(data={
            'email': 'testcom',
        })
        self.assertFalse(form.is_valid())

    def test_view_home_response(self):
        c = Client()
        respone = c.get(self.url1)
        self.assertEqual(respone.status_code, 200)

    def test_view_home_response_2(self):
        c = Client()
        respone = c.get(self.url1)
        self.assertTemplateUsed(respone, template_name='root/index.html')




    # def test_view_root(self):
    #     url1 = reverse('root:home')
    #     url2 = reverse('root:contact')
    #     url3 = reverse('root:about')
    #     url4 = reverse('root:trainer')
    #     self.assertEqual(resolve(url1).func.view_class, HomeView)
    #     self.assertEqual(resolve(url2).func, contact)
    #     self.assertEqual(resolve(url3).func, about)
    #     self.assertEqual(resolve(url4).func, trainer)

    


