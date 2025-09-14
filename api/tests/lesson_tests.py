from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.helpers.helpers import  Helpers

class LessonsForSpecificCourse(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/course'

    def test_course_lessons(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        course = Helpers.create_course(token)
        course_id = course.json()['data']['id']
        url = f'{self.url}/{course_id}/lessons'

        response = self.client.get(url, HTTP_AUTHORIZATION=token, format='json', content_type='application/json')
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(course.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LessonsListAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/lessons'

    def test_lessons_list(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        lesson, course_id = Helpers.create_lesson(token)
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=token,
            content_type='application/json', format='json',
        )
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(lesson.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateLessonAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'

    def test_create_lesson_for_course(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        response, course_id = Helpers.create_lesson(token)
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class SpecificLessonAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/lessons'

    def test_specific_lesson(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        lesson, course_id = Helpers.create_lesson(token)
        lesson_id = lesson.json()['data']['id']
        url = f'{self.url}/{lesson_id}'
        response = self.client.get(
            url, HTTP_AUTHORIZATION=token,
            content_type='application/json', format='json',
        )
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(lesson.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DeleteLessonAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/lessons'

    def test_delete_lesson(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        lesson, course_id = Helpers.create_lesson(token)
        lesson_id = lesson.json()['data']['id']
        url = f'{self.url}/{lesson_id}'
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=token,
            content_type='application/json', format='json',
        )
        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(lesson.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class MarkLessonCompleteAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/lessons'

    def test_mark_lesson_complete(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        lesson, course_id = Helpers.create_lesson(token)
        lesson_id = lesson.json()['data']['id']
        url = f'{self.url}/{lesson_id}/mark_completed'
        response = self.client.post(
            url, HTTP_AUTHORIZATION=token,
            content_type='application/json', format='json',
        )

        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(lesson.status_code, status.HTTP_201_CREATED)
        # since he is not enroll in this course => status code should be 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['errors']['detail'], 'You are not enrolled in this course.')

class UpdateLessonAPITest(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.username = 'darxx03eh'
        self.password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/lessons'

    def test_update_lesson(self):
        user = Helpers.login(self.username, self.password)
        user_data = user.json()
        token = f'Bearer {user_data['data']['access']}'
        lesson, course_id = Helpers.create_lesson(token)
        lesson_id = lesson.json()['data']['id']
        url = f'{self.url}/{lesson_id}'

        response = self.client.put(url, data={
            'title': 'test',
            'description': 'test',
            'order': 2,
            'course_id': course_id
        }, HTTP_AUTHORIZATION=token, format='multipart')

        self.assertEqual(user.status_code, status.HTTP_200_OK)
        self.assertEqual(lesson.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)