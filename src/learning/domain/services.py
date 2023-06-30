from learning.domain.repo import AdmissionRepo
from learning.domain.squad import get_nearest_squad


class GrantPremiumService:
    def __init__(self, admission_repo: AdmissionRepo):
        self.admission_repo = admission_repo

    def execute(self, admission_id: str) -> None:
        admission = self.admission_repo.get(admission_id=admission_id)
        squad = get_nearest_squad(course_id=admission.course_id)
        admission.grant_premium(squad_id=squad.id)
        self.admission_repo.save(admission=admission)
