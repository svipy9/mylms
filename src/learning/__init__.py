from django.utils import timezone

from learning.admissions.models import Admission
from learning.squads.models import Squad


def admission_grunt_premium(admission_id: int) -> None:
    admission = Admission.objects.get(id=admission_id)
    nearest_squad = (
        Squad.objects.filter(
            course=admission.course,
            start_date__gt=timezone.now(),
        )
        .order_by("start_date")
        .first()
    )

    admission.squad = nearest_squad
    admission.paid_at = timezone.now()
    admission.is_premium = True

    admission.save()


def admission_revoke_premium(admission_id: int) -> None:
    admission = Admission.objects.get(id=admission_id)

    admission.is_premium = False
    admission.paid_at = None
    admission.squad = None

    admission.save()


def is_user_has_premium_admission(user_id: int, course_id: int) -> bool:
    admission = Admission.objects.filter(user_id=user_id, course_id=course_id).first()
    if not admission:
        return False

    return admission.is_premium
