import typing
from learning.domain.admission import Admission


class AdmissionRepo(typing.Protocol):
    def get(self, admission_id: int) -> Admission:
        ...

    def save(self, admission: Admission) -> None:
        ...
