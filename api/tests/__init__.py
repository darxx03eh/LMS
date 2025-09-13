from .auth_tests import LoginAPITestCase, SignupAPITestCase, LogoutAPITestCase
from .user_tests import ProfileAPITestCase, SettingsAPITestCase
from .course_tests import (
    CourseCreateAPITest, CourseListAPITest, CourseRetrieveAPITest, CourseDeleteAPITest,
    CourseUpdateAPITest, CourseProgressAPITest, CourseFeedbackAPITest
)