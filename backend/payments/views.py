from typing import Any, cast
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import (
    CreatePaymentSerializer,
    PaymentSerializer,
)
from .services import PaymentService


# ============================================================
# CREATE PAYMENT
# ============================================================

class CreatePaymentView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        serializer = CreatePaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = cast(
            dict[str, Any],
            serializer.validated_data,
        )

        order_id = validated_data["order_id"]
        provider = validated_data["provider"]

        try:

            payment = PaymentService.create_payment(
                user=request.user,
                order_id=order_id,
                provider=provider,
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": (
                    "Payment created successfully."
                ),
                "payment": PaymentSerializer(
                    payment
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# MY PAYMENTS
# ============================================================

class PaymentListView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        payments = (
            Payment.objects
            .filter(
                user=request.user
            )
            .select_related(
                "order",
                "user",
            )
            .order_by(
                "-created_at"
            )
        )

        serializer = PaymentSerializer(
            payments,
            many=True,
        )

        return Response(
            serializer.data
        )


# ============================================================
# PAYMENT DETAIL
# ============================================================

class PaymentDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        payment_id,
    ):

        try:

            payment = (
                Payment.objects
                .select_related(
                    "order",
                    "user",
                )
                .get(
                    id=payment_id,
                    user=request.user,
                )
            )

        except Payment.DoesNotExist:

            return Response(
                {
                    "error": (
                        "Payment not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PaymentSerializer(
            payment
        )

        return Response(
            serializer.data
        )

# payments/views.py

class MarkPaymentSuccessView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, payment_id):

        try:
            payment = (
                Payment.objects
                .select_related("order")
                .get(
                    id=payment_id,
                    user=request.user,
                )
            )

        except Payment.DoesNotExist:
            return Response(
                {
                    "error": "Payment not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            payment = PaymentService.mark_payment_success(
                payment=payment,
                transaction_id=request.data.get(
                    "transaction_id"
                ),
                provider_payment_id=request.data.get(
                    "provider_payment_id"
                ),
                gateway_response={
                    "message": "Payment marked as successful.",
                    "source": "manual_test",
                },
            )

        except ValueError as error:
            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Payment marked as successful.",
                "payment": PaymentSerializer(
                    payment
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# MARK PAYMENT FAILED
# ============================================================

class MarkPaymentFailedView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, payment_id):

        try:

            payment = (
                Payment.objects
                .select_related("order")
                .get(
                    id=payment_id,
                    user=request.user,
                )
            )

        except Payment.DoesNotExist:

            return Response(
                {
                    "error": "Payment not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        reason = request.data.get(
            "reason",
            "Payment failed.",
        )

        try:

            payment = PaymentService.mark_payment_failed(
                payment=payment,
                reason=reason,
                gateway_response={
                    "message": "Payment marked as failed.",
                    "source": "manual_test",
                },
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Payment marked as failed.",
                "payment": PaymentSerializer(
                    payment
                ).data,
            },
            status=status.HTTP_200_OK,
        )