from django.db import models
from django.utils import timezone


class Squad(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_date = models.DateField()

    @classmethod
    def get_nearest(cls, course_id: int) -> "Squad":
        return (
            cls.objects.filter(
                course_id=course_id,
                start_date__gt=timezone.now(),
            )
            .order_by("start_date")
            .first()
        )
