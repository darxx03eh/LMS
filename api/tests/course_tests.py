from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.helpers.helpers import Helpers


class CourseCreateAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh',
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/courses'

    def test_create_course(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        course = Helpers.create_course(f'Bearer {user_data['data']['access']}')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(course.status_code, status.HTTP_201_CREATED)

class CourseListAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh',
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/courses?search=python'

    def test_list_course(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        course = Helpers.create_course(f'Bearer {user_data['data']['access']}')
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {user_data['data']['access']}')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(course.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CourseRetrieveAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/courses'

    def test_retrieve_course(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        course = Helpers.create_course(token)
        course_id =  course.json()['data']['id']
        url = f'{self.url}/{course_id}'
        response = self.client.get(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(course.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CourseDeleteAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/courses'

    def test_delete_course(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        course = Helpers.create_course(token)
        course_id = course.json()['data']['id']
        url = f'{self.url}/{course_id}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(course.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CourseUpdateAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/courses'

    def test_update_course(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        course = Helpers.create_course(token)
        course_id = course.json()['data']['id']
        url = f'{self.url}/{course_id}'
        payload = {
            'title': 'introduction to java programming',
            'description': 'Java programming',
            'category': 'programming',
            'level': 'beginner',
            'lessons': [
                {
                    'title': 'java',
                    'description': 'Java programming',
                    'order': 1
                }
            ]
        }

        response = self.client.put(url, data=payload, HTTP_AUTHORIZATION=token, content_type='application/json')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(course.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CourseProgressAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/courses'

    def test_course_progress(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        course = Helpers.create_course(token)
        course_id = course.json()['data']['id']
        url = f'{self.url}/{course_id}/progress'

        response = self.client.get(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(course.status_code, status.HTTP_201_CREATED)
        # not enroll in this course then 403 forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['errors']['detail'], 'You are not enrolled in this course.')

class CourseFeedbackAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/courses'

    def test_course_feedback(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        course = Helpers.create_course(token)
        course_id = course.json()['data']['id']
        url = f'{self.url}/{course_id}/feedbacks'

        response = self.client.get(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(course.status_code, status.HTTP_201_CREATED)
        # no feedbacks added yet => 404 not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)