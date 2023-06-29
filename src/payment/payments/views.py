from django.utils import timezone
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import learning.interface as learning
from payment.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "admission", "url", "status"]


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
        if (
            learning.admission_learning_started(payment.admission_id)
            <= timezone.now().date()
        ):
            return Response(
                status=400, data=dict(error="You have already started to learn.")
            )

        refund = payment.mark_refunded()

        return Response(status=200, data=dict(id=refund.id))
