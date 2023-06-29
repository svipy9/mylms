from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views.student import UserDetailView, AdmissionViewSet, CourseViewSet

student_router = DefaultRouter()
student_router.register(r'admissions', AdmissionViewSet)


manager_router = DefaultRouter()
manager_router.register(r'courses', CourseViewSet)


urlpatterns = [
    path('', include(student_router.urls)),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('mng/', include(manager_router.urls)),
    path('admin/', admin.site.urls),
]
