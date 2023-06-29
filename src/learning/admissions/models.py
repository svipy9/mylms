from django.db import models
from django.utils import timezone
from learning.squads.models import Squad


class Admission(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="unique_admission")
        ]  # Rule #1

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", null=True, on_delete=models.SET_NULL)
    squad = models.ForeignKey("squads.Squad", null=True, on_delete=models.SET_NULL)

    is_premium = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} admitted to {self.course.name}"

    @classmethod
    def find_by_user_and_course(cls, *, user_id, course_id):
        return cls.objects.filter(user_id=user_id, course_id=course_id).first()

    def grant_premium(self):
        self.squad = Squad.get_nearest(self.course_id)
        self.paid_at = timezone.now()
        self.is_premium = True

        self.save()

    def revoke_premium(self):
        self.is_premium = False
        self.paid_at = None
        self.squad = None

        self.save()
