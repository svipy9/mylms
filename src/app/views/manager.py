from rest_framework import viewsets
from app.models import Course
from app.serializers import CourseSerializer
from app.permissions import IsManagerUser


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsManagerUser]
