from Scripts.bottle import response
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from api.models import User

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.username = 'darxx03eh'
        self.password = 'mahmoud003+-'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.url = reverse('login')

    def test_login(self):
        payload = {
            'username_or_email': self.username,
            'password': self.password,
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SignupAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('signup')

    def test_signup(self):
        payload = {
            'email': 'darxx03eh@gmail.com',
            'username': 'darxx03eh',
            'password': '123456789mmm+-',
            'first_name': 'Mahmoud',
            'last_name': 'Darawsheh',
            'phone_number': '+972568249300',
            'role': 'instructor'
        }
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LogoutAPITestCase(APITestCase):
    def setUp(self):
        self.username = 'darxx03eh'
        self.password = 'mahmoud003+-'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login = reverse('login')
        self.logout = reverse('logout')

    def test_logout(self):
        user = self.client.post(self.login, data={
            'username_or_email': self.username,
            'password': self.password,
        })
        user_data = user.json()
        response = self.client.post(self.logout, data={
            'refresh': f'{user_data['data']['refresh']}'
        }, HTTP_AUTHORIZATION=f'Bearer {user_data['data']['access']}')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)