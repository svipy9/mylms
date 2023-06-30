# APIView that grants premium admission to a user
from rest_framework.response import Response
from rest_framework.views import APIView
from learning.domain.services import GrantPremiumService
from learning.infra.admissions.repo import DjangoAdmissionRepo


class GrantPremiumAdmissionView(APIView):
    def post(self, request, admission_id):
        repo = DjangoAdmissionRepo()
        GrantPremiumService(repo).execute(admission_id=admission_id)
        return Response(status=200)
