from rest_framework import mixins, permissions, serializers, viewsets

import learning.interface as learning
from accounts.permissions import IsManagerUser
from content.courses.models import Course, Lesson


class ManagerCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "slug", "description", "price"]


class ManagerCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = ManagerCourseSerializer
    permission_classes = [IsManagerUser]


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ["id", "name", "slug", "description", "price"]
        fields = read_only_fields


class StudentLessonSerializer(serializers.ModelSerializer):
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


class StudentCourseDetailSerializer(StudentCourseSerializer):
    class Meta(StudentCourseSerializer.Meta):
        read_only_fields = StudentCourseSerializer.Meta.read_only_fields + ["lessons"]
        fields = read_only_fields

    lessons = serializers.SerializerMethodField()

    def get_lessons(self, course):
        user = self.context["request"].user

        self.context["is_premium"] = learning.is_user_has_premium_admission(
            user.id, course.id
        )

        serializer = StudentLessonSerializer(
            course.lesson_set.all(),
            context=self.context,
            many=True,
        )

        return serializer.data


class StudentCourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Course.objects.all()
    serializer_class = StudentCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudentCourseDetailSerializer
        return StudentCourseSerializer
