from django.db import models


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
