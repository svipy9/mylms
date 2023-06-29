from rest_framework import viewsets

from courses.models import Course, Lesson
from accounts.permissions import IsManagerUser
from rest_framework import serializers, mixins, permissions


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
        admission = Admission.objects.filter(user=user, course=course).first()
        if admission and admission.is_premium:
            self.context["is_premium"] = True

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
        if self.action == "retrieve":  # The action is 'retrieve' for the detail view.
            return CourseDetailSerializer  # Use CourseDetailSerializer for the detail view.
        return CourseSerializer  # Use CourseSerializer for all other views.