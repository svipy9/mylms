from django.utils import timezone

from learning.admissions.models import Admission
from learning.squads.models import Squad


def admission_grunt_premium(admission_id: int):
    admission = Admission.objects.get(id=admission_id)
    nearest_squad = Squad.objects.filter(
        course=admission.course,
        start_date__gt=timezone.now(),
    ).order_by("start_date").first()

    admission.squad = nearest_squad
    admission.paid_at = timezone.now()
    admission.is_premium = True

    admission.save()


def admission_revoke_premium(admission_id: int):
    admission = Admission.objects.get(id=admission_id)

    admission.is_premium = False
    admission.paid_at = None
    admission.squad = None

    admission.save()
