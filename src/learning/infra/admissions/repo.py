from learning.infra.admissions.models import Admission as AdmissionModel
from learning.domain.admission import Admission


class DjangoAdmissionRepo():
    def __init__(self):
        self.model = AdmissionModel

    def get(self, admission_id: str) -> Admission:
        admission = self.model.objects.get(id=admission_id)
        return Admission(
            admission_id=admission.id,
            student_id=admission.student_id,
            course_id=admission.course_id,
            status=admission.status,
            created_at=admission.created_at,
            updated_at=admission.updated_at
        )

    def save(self, admission: Admission) -> Admission:
        admission, _ = self.model.objects.update_or_create(
            student_id=admission.student_id,
            course_id=admission.course_id,
            status=admission.status
        )
        return Admission(
            admission_id=admission.id,
            student_id=admission.student_id,
            course_id=admission.course_id,
            status=admission.status,
            created_at=admission.created_at,
            updated_at=admission.updated_at
        )
