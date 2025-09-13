from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from api.models import User

class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.username = 'darxx03eh'
        self.password = 'mahmoud003+-'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.url = reverse('profile')
        self.login = reverse('login')

    def test_profile(self):
        payload = {
            'username_or_email': self.username,
            'password': self.password,
        }

        user = self.client.post(self.login, data=payload)
        user_data = user.json()
        profile = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {user_data['data']['access']}')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.status_code, status.HTTP_200_OK)

class SettingsAPITestCase(APITestCase):
    def setUp(self):
        self.username = 'darxx03eh'
        self.password = 'mahmoud003+-'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.login = reverse('login')
        self.url = reverse('profile')

    def test_profile(self):
        payload = {
            'username_or_email': self.username,
            'password': self.password
        }

        user = self.client.post(self.login, data=payload)
        user_data = user.json()

        settings = self.client.patch(self.url, data={
            'first_name': 'Mahmoud',
            'last_name': 'Darawsheh',
            'email': 'darxx03eh@gmail.com',
            'phone_number': '+972568249300',
        }, HTTP_AUTHORIZATION=f'Bearer {user_data['data']['access']}')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(settings.status_code, status.HTTP_200_OK)