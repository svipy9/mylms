from rest_framework import viewsets

from app.models import Course
from app.permissions import IsManagerUser
from app.serializers.manager import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsManagerUser]
