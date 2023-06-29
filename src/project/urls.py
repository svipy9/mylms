from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from schema_graph.views import Schema

from app.views import student
from app.views.manager import CourseViewSet

student_router = DefaultRouter()
student_router.register(r"admissions", student.AdmissionViewSet)
student_router.register(r"courses", student.CourseViewSet)


manager_router = DefaultRouter()
manager_router.register(r"courses", CourseViewSet)


urlpatterns = [
    path("login/", student.LoginView.as_view(), name="account_login"),
    path("", include(student_router.urls)),
    path("me/", student.UserDetailView.as_view(), name="user-detail"),
    path("mng/", include(manager_router.urls)),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    path("schema/", Schema.as_view()),
]
