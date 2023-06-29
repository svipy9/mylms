from rest_framework import serializers

from app.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "slug", "description", "price"]
