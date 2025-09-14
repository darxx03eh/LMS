from Scripts.bottle import response
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.helpers.helpers import Helpers


class CreateFeedbackTests(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.instructor_username = 'darxx03eh'
        self.instructor_password = '123456789mmm+-'
        Helpers.create_student_account()
        self.student_username = 'darawsheh'
        self.student_password = '123456789mmm+-'

    def test_create_feedback(self):
        instructor = Helpers.login(self.instructor_username, self.instructor_password)
        instructor_data = instructor.json()
        instructor_token = f'Bearer {instructor_data['data']['access']}'
        student = Helpers.login(self.student_username, self.student_password)
        student_data = student.json()
        student_token = f'Bearer {student_data['data']['access']}'

        feedback, feedback_id, course_id = Helpers.create_feedback(instructor_token, student_token)

        self.assertEqual(instructor.status_code, status.HTTP_200_OK)
        self.assertEqual(student.status_code, status.HTTP_200_OK)
        self.assertEqual(feedback.status_code, status.HTTP_201_CREATED)

class FeedBackListTests(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.instructor_username = 'darxx03eh'
        self.instructor_password = '123456789mmm+-'
        Helpers.create_student_account()
        self.student_username = 'darawsheh'
        self.student_password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/feedbacks'

    def test_list_feedback(self):
        instructor = Helpers.login(self.instructor_username, self.instructor_password)
        instructor_data = instructor.json()
        instructor_token = f'Bearer {instructor_data['data']['access']}'
        student = Helpers.login(self.student_username, self.student_password)
        student_data = student.json()
        student_token = f'Bearer {student_data['data']['access']}'

        feedback, feedback_id, course_id = Helpers.create_feedback(instructor_token, student_token)
        response = self.client.get(self.url, HTTP_AUTHORIZATION=student_token, content_type='application/json')

        self.assertEqual(instructor.status_code, status.HTTP_200_OK)
        self.assertEqual(student.status_code, status.HTTP_200_OK)
        self.assertEqual(feedback.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SpecificFeedbackTests(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.instructor_username = 'darxx03eh'
        self.instructor_password = '123456789mmm+-'
        Helpers.create_student_account()
        self.student_username = 'darawsheh'
        self.student_password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/feedbacks'

    def test_specific_feedback(self):
        instructor = Helpers.login(self.instructor_username, self.instructor_password)
        instructor_data = instructor.json()
        instructor_token = f'Bearer {instructor_data['data']['access']}'
        student = Helpers.login(self.student_username, self.student_password)
        student_data = student.json()
        student_token = f'Bearer {student_data['data']['access']}'

        feedback, feedback_id, course_id = Helpers.create_feedback(instructor_token, student_token)
        url = f'{self.url}/{feedback_id}'
        response = self.client.get(url, HTTP_AUTHORIZATION=student_token, content_type='application/json')

        self.assertEqual(instructor.status_code, status.HTTP_200_OK)
        self.assertEqual(student.status_code, status.HTTP_200_OK)
        self.assertEqual(feedback.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UpdateFeedbackTests(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.instructor_username = 'darxx03eh'
        self.instructor_password = '123456789mmm+-'
        Helpers.create_student_account()
        self.student_username = 'darawsheh'
        self.student_password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/feedbacks'

    def test_update_feedback(self):
        instructor = Helpers.login(self.instructor_username, self.instructor_password)
        instructor_data = instructor.json()
        instructor_token = f'Bearer {instructor_data['data']['access']}'
        student = Helpers.login(self.student_username, self.student_password)
        student_data = student.json()
        student_token = f'Bearer {student_data['data']['access']}'

        feedback, feedback_id, course_id = Helpers.create_feedback(instructor_token, student_token)
        url = f'{self.url}/{feedback_id}'
        response = self.client.put(url, data={
            'rate': 1,
            'comment': 'this course is so bad',
            'course_id': course_id
        }, HTTP_AUTHORIZATION=student_token, content_type='application/json')

        self.assertEqual(instructor.status_code, status.HTTP_200_OK)
        self.assertEqual(student.status_code, status.HTTP_200_OK)
        self.assertEqual(feedback.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DeleteFeedbackTests(APITestCase):
    def setUp(self):
        Helpers.signup()
        self.instructor_username = 'darxx03eh'
        self.instructor_password = '123456789mmm+-'
        Helpers.create_student_account()
        self.student_username = 'darawsheh'
        self.student_password = '123456789mmm+-'
        self.url = 'http://127.0.0.1:8000/api/v1/feedbacks'

    def test_delete_feedback(self):
        instructor = Helpers.login(self.instructor_username, self.instructor_password)
        instructor_data = instructor.json()
        instructor_token = f'Bearer {instructor_data['data']['access']}'
        student = Helpers.login(self.student_username, self.student_password)
        student_data = student.json()
        student_token = f'Bearer {student_data['data']['access']}'

        feedback, feedback_id, course_id = Helpers.create_feedback(instructor_token, student_token)
        url = f'{self.url}/{feedback_id}'
        response = self.client.delete(url, HTTP_AUTHORIZATION=student_token, content_type='application/json')

        self.assertEqual(instructor.status_code, status.HTTP_200_OK)
        self.assertEqual(student.status_code, status.HTTP_200_OK)
        self.assertEqual(feedback.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)