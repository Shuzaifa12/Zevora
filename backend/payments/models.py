from decimal import Decimal

from django.conf import settings
from django.db import models


class Payment(models.Model):

    # ========================================================
    # PAYMENT STATUS
    # ========================================================

    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_SUCCEEDED = "succeeded"
    STATUS_FAILED = "failed"
    STATUS_CANCELLED = "cancelled"
    STATUS_REFUNDED = "refunded"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_SUCCEEDED, "Succeeded"),
        (STATUS_FAILED, "Failed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_REFUNDED, "Refunded"),
    ]

    # ========================================================
    # PAYMENT PROVIDERS
    # ========================================================

    PROVIDER_COD = "cod"
    PROVIDER_ONLINE = "online"

    PROVIDER_CHOICES = [
        (PROVIDER_COD, "Cash on Delivery"),
        (PROVIDER_ONLINE, "Online Card Payment"),
    ]

    # ========================================================
    # RELATIONSHIPS
    # ========================================================

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="payments",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    # ========================================================
    # PAYMENT DETAILS
    # ========================================================

    provider = models.CharField(
        max_length=30,
        choices=PROVIDER_CHOICES,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    currency = models.CharField(
        max_length=3,
        default="PKR",
    )

    # ========================================================
    # TRANSACTION INFORMATION
    # ========================================================

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    provider_payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )

    # ========================================================
    # GATEWAY DATA
    # ========================================================

    gateway_response = models.JSONField(
        blank=True,
        null=True,
    )

    failure_reason = models.TextField(
        blank=True,
    )

    # ========================================================
    # REFUND INFORMATION
    # ========================================================

    refunded_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "order",
                    "-created_at",
                ]
            ),

            models.Index(
                fields=[
                    "user",
                    "-created_at",
                ]
            ),

            models.Index(
                fields=[
                    "status",
                ]
            ),

            models.Index(
                fields=[
                    "provider",
                ]
            ),
        ]

    def __str__(self):
        return (
            f"{self.order.order_number} - "
            f"{self.provider} - "
            f"{self.status}"
        )