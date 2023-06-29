from django.db import models


class Squad(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_date = models.DateField()
