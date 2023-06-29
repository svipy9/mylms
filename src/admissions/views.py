from admissions.models import Admission
from rest_framework import mixins, permissions, viewsets, serializers
from accounts.permissions import IsManagerUser
from django.utils import timezone
from squads.models import Squad



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
            validated_data["paid_at"] = timezone.now()
            nearest_squad = Squad.objects.filter(
                course=admission.course,
                start_date__gt=timezone.now(),
            ).first()
            validated_data["squad"] = nearest_squad  # Rule #3

        if not validated_data.get(
            "is_premium"
        ) and admission.is_premium != validated_data.get("is_premium"):
            validated_data["paid_at"] = None
            validated_data["squad"] = None

        return super().update(admission, validated_data)


class ManagerAdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = ManagerAdmissionSerializer
    permission_classes = [IsManagerUser]
