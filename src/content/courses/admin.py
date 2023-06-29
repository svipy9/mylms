from django.contrib import admin

from content.courses.models import Course, Lesson

admin.site.register(Lesson)
admin.site.register(Course)
