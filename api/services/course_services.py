from api.models import Course, User


class CourseServices:
    def calculate_progress(self, course_id, user: User):
        course = Course.objects.get(id=course_id)
        total_lessons = course.lessons.count()
        completed_lessons = course.lessons.filter(
            students__completed_lessons_courses__students=user
        ).count()

        if total_lessons == 0:
            return f"your progress in {course.title} is {00}"
        return f"your progress in {course.title} is {(completed_lessons / total_lessons) * 100}"
