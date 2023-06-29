from django.utils import timezone
from rest_framework import serializers

from app.models import Admission, Course, Squad


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "slug", "description", "price"]


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        read_only_fields = ["id", "course", "user", "paid_at", "squad"]
        fields = read_only_fields + ["is_premium"]

    def update(self, admission, validated_data):
        # Buisness Rule 2:

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
