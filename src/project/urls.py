from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from schema_graph.views import Schema

from accounts.views import UserDetailView, LoginView
from admissions.views import StudentAdmissionViewSet, ManagerAdmissionViewSet
from courses.views import StudentCourseViewSet, ManagerCourseViewSet
from payments.views import PaymentViewSet

student_router = DefaultRouter()
student_router.register(r"admissions", StudentAdmissionViewSet)
student_router.register(r"courses", StudentCourseViewSet)
student_router.register(r"payments", PaymentViewSet)


manager_router = DefaultRouter()
manager_router.register(r"courses", ManagerCourseViewSet)
manager_router.register(r"admissions", ManagerAdmissionViewSet)


urlpatterns = [
    path("login/", LoginView.as_view(), name="account_login"),
    path("", include(student_router.urls)),
    path("me/", UserDetailView.as_view(), name="user-detail"),
    path("mng/", include(manager_router.urls)),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    path("schema/", Schema.as_view()),
]
