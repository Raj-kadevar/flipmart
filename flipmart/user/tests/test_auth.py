from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from user.models import User
# client = Client()

class RegistrationTest(TestCase):
    url = reverse('registration')
    def setUp(self):
        self.user_data = {'name': "testt",'password1':"123",'password2':"123"}
        self.user_missmatch_data = {'username': "testt",'password1':"123",'password2':"1234"}
        self.user_valid_data = {'username': "demo",'password1':"123.@qwe",'password2':"123.@qwe"}

    def test_user_register_invalid(self):
        form_status = self.client.post(self.url, data=self.user_data)
        self.assertEquals(form_status.status_code, 400)

    def test_user_register_missmatch(self):
        form_status = self.client.post(self.url, data=self.user_missmatch_data)
        self.assertEquals(form_status.status_code, 400)

    def test_user_register(self):
        form_status = self.client.post(self.url, data=self.user_valid_data)
        self.assertEquals(form_status.status_code, 302)

class LoginTest(TestCase):
    url = reverse('login')
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='1234')
        self.login_detail = {'username': "test",'password':"1234"}
        self.incorrect_login_detail = {'username': "raj",'password':"abcd"}
        self.invalid_login_detail = {'password':"123"}

    def test_user_invalid_login(self):
        login_status = self.client.post(self.url, data=self.invalid_login_detail)
        self.assertEquals(login_status.status_code, 400)

    def test_incorrect_user(self):
        login_status = self.client.post(self.url, data=self.incorrect_login_detail)
        self.assertEquals(login_status.status_code, 400)

    def test_empty_data(self):
        login_status = self.client.post(self.url, data={})
        self.assertEquals(login_status.status_code, 400)

    def test_user_login(self):
        login_status = self.client.post(self.url, data=self.login_detail)
        self.assertEquals(login_status.status_code, 302)