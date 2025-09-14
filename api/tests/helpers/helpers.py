from django.test.testcases import Client
from django.urls import reverse
from django.conf import settings
import os
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
    def create_student_account():
        client = Client()
        payload = {
            'email': 'darawsheh003@gmail.com',
            'username': 'darawsheh',
            'password': '123456789mmm+-',
            'first_name': 'Mahmoud',
            'last_name': 'Darawsheh',
            'phone_number': '+970568249300',
            'role': 'student'
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

    @staticmethod
    def create_lesson(token):
        client = Client()
        url = 'http://127.0.0.1:8000/api/v1/lessons'
        course = Helpers.create_course(token)
        course_id = course.json()['data']['id']
        lesson = client.post(url, data={
            'title': 'this is a lessons title',
            'description': 'this is a lessons description',
            'order': 1,
            'course_id': course_id,
            'video': open(os.path.join(
                settings.MEDIA_ROOT, 'lessons/videos/Macbook-Air-araboon.vercel.app-mjo4zkarphl5ai.webm')),
            'document': open(os.path.join(settings.MEDIA_ROOT, 'lessons/docs/ARABOON.postman_collection.json'))
        }, format='multipart', HTTP_AUTHORIZATION=token)
        return (lesson, course_id)

    @staticmethod
    def create_feedback(instructor_token, student_token):
        client = Client()
        url = 'http://127.0.0.1:8000/api/v1/courses/feedback'
        course = Helpers.create_course(instructor_token)
        course_id = course.json()['data']['id']
        feedback = client.post(url, data={
            'rate': 5,
            'comment': 'best course ever',
            'course_id': course_id
        }, HTTP_AUTHORIZATION=student_token, content_type='application/json')

        return feedback, feedback.json()['data']['id'], course_id