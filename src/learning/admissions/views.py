from django.utils import timezone
from rest_framework import mixins, permissions, serializers, viewsets

from accounts.permissions import IsManagerUser
from learning.admissions.models import Admission
from learning.squads.models import Squad


class StudentAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ["id", "user", "course", "created_at", "is_premium", "paid_at"]
        read_only_fields = ["is_premium", "paid_at", "user"]


class StudentAdmissionViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Admission.objects.all()
    serializer_class = StudentAdmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Rule #2

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ManagerAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        read_only_fields = ["id", "course", "user", "paid_at", "squad"]
        fields = read_only_fields + ["is_premium"]

    def update(self, admission, validated_data):
        # Buisness Rule 2
        if validated_data.get(
            "is_premium"
        ) and admission.is_premium != validated_data.get("is_premium"):
            admission.grant_premium()  # Rule #3

        if not validated_data.get(
            "is_premium"
        ) and admission.is_premium != validated_data.get("is_premium"):
            admission.revoke_premium()

        return super().update(admission, validated_data)


class ManagerAdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = ManagerAdmissionSerializer
    permission_classes = [IsManagerUser]
