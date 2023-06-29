from learning.admissions.models import Admission


def admission_grant_premium(admission_id: int) -> None:
    admission = Admission.objects.get(id=admission_id)
    admission.grant_premium()


def admission_revoke_premium(admission_id: int) -> None:
    admission = Admission.objects.get(id=admission_id)
    admission.revoke_premium()


def is_user_has_premium_admission(user_id: int, course_id: int) -> bool:
    admission = Admission.find_by_user_and_course(user_id=user_id, course_id=course_id)
    if not admission:
        return False

    return admission.is_premium
