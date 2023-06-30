from datetime import date
from typing import Optional

from learning.admissions.models import Admission
from learning.squads.models import Squad


def admission_grant_premium(admission_id: int) -> None:
    admission = Admission.objects.get(id=admission_id)
    squad = Squad.get_nearest_squad(admission.course_id)
    admission.grant_premium(squad_id=squad.id)


def admission_revoke_premium(admission_id: int) -> None:
    admission = Admission.objects.get(id=admission_id)
    admission.revoke_premium()


def is_user_has_premium_admission(user_id: int, course_id: int) -> bool:
    admission = Admission.find_by_user_and_course(user_id=user_id, course_id=course_id)
    if not admission:
        return False

    return admission.is_premium


def admission_learning_started(admission_id: int) -> Optional[date]:
    admission = Admission.objects.get(id=admission_id)

    return admission.squad.start_date if admission.squad else None
