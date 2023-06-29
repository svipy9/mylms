from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Admission, Course, Lesson, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "is_manager"]


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ["id", "user", "course", "created_at", "is_premium", "paid_at"]
        read_only_fields = ["is_premium", "paid_at", "user"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ["id", "name", "slug", "description", "price"]
        fields = read_only_fields


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        read_only_fields = ["id", "name", "is_free", "content"]
        fields = read_only_fields

    content = serializers.SerializerMethodField()

    def get_content(self, lesson):
        # Rule #4
        if lesson.is_free or self.context.get("is_premium"):
            return lesson.content
        return None


class CourseDetailSerializer(CourseSerializer):
    class Meta(CourseSerializer.Meta):
        read_only_fields = CourseSerializer.Meta.read_only_fields + ["lessons"]
        fields = read_only_fields

    lessons = serializers.SerializerMethodField()

    def get_lessons(self, course):
        user = self.context["request"].user
        admission = Admission.objects.filter(user=user, course=course).first()
        if admission and admission.is_premium:
            self.context["is_premium"] = True

        serializer = LessonSerializer(
            course.lesson_set.all(),
            context=self.context,
            many=True,
        )

        return serializer.data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "admission", "url", "status"]
