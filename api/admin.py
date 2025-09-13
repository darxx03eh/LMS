from django.contrib import admin

from .models import CompletedLesson, Course, Enrollment, Feedback, Lesson, User


# Register your models here.
class LessonsInline(admin.TabularInline):
    model = Lesson


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonsInline]


admin.site.register(User)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Feedback)
admin.site.register(CompletedLesson)
