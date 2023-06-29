from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.name} ({self.slug})"


class Lesson(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    is_free = models.BooleanField(default=False)
