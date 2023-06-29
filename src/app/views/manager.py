from rest_framework import viewsets

from app.models import Admission, Course
from app.permissions import IsManagerUser
from app.serializers.manager import AdmissionSerializer, CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsManagerUser]


class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    permission_classes = [IsManagerUser]
