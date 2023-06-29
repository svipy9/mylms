from django.contrib.auth import authenticate, login
from django.utils import timezone
from rest_framework import generics, mixins, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Admission, Course, Payment, Refund
from app.serializers.student import (
    AdmissionSerializer,
    CourseDetailSerializer,
    CourseSerializer,
    PaymentSerializer,
    UserSerializer,
)


class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Login Successful"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AdmissionViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Rule #2

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":  # The action is 'retrieve' for the detail view.
            return CourseDetailSerializer  # Use CourseDetailSerializer for the detail view.
        return CourseSerializer  # Use CourseSerializer for all other views.


class PaymentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(admission__user=self.request.user)

    @action(detail=True, methods=["post"])
    def refund(self, request, **_):
        payment = self.get_object()

        # Rule #5: user can't create refund when he started to learn.
        if payment.admission.squad.start_date <= timezone.now().date():
            return Response(
                status=400, data=dict(error="You have already started to learn.")
            )

        refund = Refund.objects.create(payment=payment)

        return Response(status=200, data=dict(id=refund.id))
