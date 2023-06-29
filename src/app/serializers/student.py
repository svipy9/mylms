from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Admission, Course


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "is_manager"]


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ["id", "user", "course", "created_at", "paid", "paid_at"]
        read_only_fields = ["paid", "paid_at", "user"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ["id", "name", "slug", "description", "price"]
        fields = read_only_fields
