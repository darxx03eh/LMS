from django.test.testcases import Client
from django.urls import reverse
class Helpers:
    @staticmethod
    def login(username, password):
        client = Client()
        payload = {
            'username_or_email': username,
            'password': password
        }

        return client.post(reverse('login'), data=payload)

    @staticmethod
    def signup():
        client = Client()
        payload = {
            'email': 'darxx03eh@gmail.com',
            'username': 'darxx03eh',
            'password': '123456789mmm+-',
            'first_name': 'Mahmoud',
            'last_name': 'Darawsheh',
            'phone_number': '+972568249300',
            'role': 'instructor'
        }

        client.post(reverse('signup'), data=payload)
        return

    @staticmethod
    def create_course(token):
        client = Client()
        url = 'http://127.0.0.1:8000/api/v1/courses'
        course = client.post(url, data={
            'title': 'introduction to python programming',
            'description': 'Python programming',
            'category': 'programming',
            'level': 'beginner',
            'lessons': [
                {
                    'title': 'python',
                    'description': 'Python programming',
                    'order': 1
                }
            ]
        }, HTTP_AUTHORIZATION=f'{token}', format='json', content_type='application/json')
        return course