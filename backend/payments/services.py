from django.db import transaction
from django.utils import timezone

from orders.models import Order

from .models import Payment


class PaymentService:

    @staticmethod
    @transaction.atomic
    def create_payment(
        *,
        user,
        order_id,
        provider,
    ):
        """
        Create a payment record for an order.

        Security:
        - User can only access their own order.
        - Amount always comes from Order.total.
        - Frontend cannot modify amount.
        - Cancelled orders cannot be paid.
        - Already paid orders cannot be paid again.
        """

        try:
            order = (
                Order.objects
                .select_for_update()
                .get(
                    id=order_id,
                    user=user,
                )
            )

        except Order.DoesNotExist:
            raise ValueError(
                "Order not found or you do not have permission to access it."
            )

        if order.status == Order.STATUS_CANCELLED:
            raise ValueError(
                "Payment cannot be created for a cancelled order."
            )

        if order.payment_status == Order.PAYMENT_PAID:
            raise ValueError(
                "This order has already been paid."
            )

        # ----------------------------------------------------
        # Validate provider
        # ----------------------------------------------------

        allowed_providers = [
            Payment.PROVIDER_COD,
            Payment.PROVIDER_CARD,
            Payment.PROVIDER_ONLINE,
        ]

        if provider not in allowed_providers:
            raise ValueError(
                "Unsupported payment provider."
            )

        # ----------------------------------------------------
        # Prevent duplicate COD payment records
        # ----------------------------------------------------

        if provider == Payment.PROVIDER_COD:

            existing_cod_payment = (
                Payment.objects
                .filter(
                    order=order,
                    provider=Payment.PROVIDER_COD,
                    status__in=[
                        Payment.STATUS_PENDING,
                        Payment.STATUS_PROCESSING,
                    ],
                )
                .first()
            )

            if existing_cod_payment:
                return existing_cod_payment

        # ----------------------------------------------------
        # Create payment record
        # ----------------------------------------------------

        payment = Payment.objects.create(
            order=order,
            user=user,
            provider=provider,
            status=Payment.STATUS_PENDING,
            amount=order.total,
            currency="PKR",
            gateway_response={
                "message": "Payment record created.",
            },
        )

        # Keep Order.payment_method synchronized
        if provider == Payment.PROVIDER_COD:
            order.payment_method = Order.PAYMENT_COD

        elif provider == Payment.PROVIDER_CARD:
            order.payment_method = Order.PAYMENT_CARD

        elif provider == Payment.PROVIDER_ONLINE:
            order.payment_method = Order.PAYMENT_ONLINE

        order.save(
            update_fields=[
                "payment_method",
                "updated_at",
            ]
        )

        return payment

    # ========================================================
    # PAYMENT SUCCESS
    # ========================================================

    @staticmethod
    @transaction.atomic
    def mark_payment_success(
        *,
        payment,
        transaction_id=None,
        provider_payment_id=None,
        gateway_response=None,
    ):
        """
        Mark payment as successful and synchronize the order.
        """

        payment = (
            Payment.objects
            .select_for_update()
            .select_related("order")
            .get(id=payment.id)
        )

        # Idempotency:
        # Duplicate webhook should not update payment again.
        if payment.status == Payment.STATUS_SUCCEEDED:
            return payment

        payment.status = Payment.STATUS_SUCCEEDED

        if transaction_id:
            payment.transaction_id = transaction_id

        if provider_payment_id:
            payment.provider_payment_id = provider_payment_id

        if gateway_response is not None:
            payment.gateway_response = gateway_response

        payment.save(
            update_fields=[
                "status",
                "transaction_id",
                "provider_payment_id",
                "gateway_response",
                "updated_at",
            ]
        )

        order = (
            Order.objects
            .select_for_update()
            .get(id=payment.order_id) # type: ignore
        )

        order.payment_status = Order.PAYMENT_PAID

        order.transaction_id = (
            transaction_id
            or provider_payment_id
            or payment.transaction_id
        )

        order.paid_at = timezone.now()

        if order.status == Order.STATUS_PENDING:
            order.status = Order.STATUS_CONFIRMED

        order.save(
            update_fields=[
                "payment_status",
                "transaction_id",
                "paid_at",
                "status",
                "updated_at",
            ]
        )

        return payment

    # ========================================================
    # PAYMENT FAILURE
    # ========================================================

    @staticmethod
    @transaction.atomic
    def mark_payment_failed(
        *,
        payment,
        reason="",
        gateway_response=None,
    ):
        """
        Mark payment as failed and synchronize the order.
        """

        payment = (
            Payment.objects
            .select_for_update()
            .get(id=payment.id)
        )

        # ----------------------------------------------------
        # PREVENT INVALID STATE CHANGE
        # ----------------------------------------------------

        if payment.status == Payment.STATUS_SUCCEEDED:
            raise ValueError(
                "A successful payment cannot be marked as failed."
            )

        # ----------------------------------------------------
        # UPDATE PAYMENT
        # ----------------------------------------------------

        payment.status = Payment.STATUS_FAILED
        payment.failure_reason = reason

        if gateway_response is not None:
            payment.gateway_response = gateway_response

        payment.save(
            update_fields=[
                "status",
                "failure_reason",
                "gateway_response",
                "updated_at",
            ]
        )

        # ----------------------------------------------------
        # UPDATE ORDER
        # ----------------------------------------------------

        order = (
            Order.objects
            .select_for_update()
            .get(id=payment.order_id) # type: ignore
        )

        order.payment_status = Order.PAYMENT_FAILED

        order.save(
            update_fields=[
                "payment_status",
                "updated_at",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def cancel_payment(*, payment):
        payment = (
            Payment.objects
            .select_for_update()
            .get(id=payment.id)
        )

        if payment.status == Payment.STATUS_SUCCEEDED:
            raise ValueError(
                "A successful payment cannot be cancelled. "
                "Refund is required."
            )

        if payment.status == Payment.STATUS_REFUNDED:
            raise ValueError(
                "A refunded payment cannot be cancelled."
            )

        if payment.status == Payment.STATUS_CANCELLED:
            # Still synchronize Order.
            order = (
                Order.objects
                .select_for_update()
                .get(id=payment.order_id) # type: ignore
            )

            if order.payment_status != Order.PAYMENT_CANCELLED:
                order.payment_status = Order.PAYMENT_CANCELLED

                order.save(
                    update_fields=[
                        "payment_status",
                        "updated_at",
                    ]
                )
            return payment

        payment.status = Payment.STATUS_CANCELLED

        payment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        # Update related order payment status
        order = (
            Order.objects
            .select_for_update()
            .get(id=payment.order_id) # type: ignore
        )

        order.payment_status = Order.PAYMENT_CANCELLED # type: ignore

        order.save(
            update_fields=[
                "payment_status",
                "updated_at",
            ]
        )

        return payment