from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class Order(models.Model):
    # ========================================================
    # ORDER STATUS
    # ========================================================

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_SHIPPED, "Shipped"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    # ========================================================
    # PAYMENT STATUS
    # ========================================================

    PAYMENT_PENDING = "pending"
    PAYMENT_PAID = "paid"
    PAYMENT_FAILED = "failed"
    PAYMENT_REFUNDED = "refunded"
    PAYMENT_CANCELLED = "cancelled"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, "Pending"),
        (PAYMENT_PAID, "Paid"),
        (PAYMENT_FAILED, "Failed"),
        (PAYMENT_REFUNDED, "Refunded"),
        (PAYMENT_CANCELLED, "Cancelled"),
    ]

    # ========================================================
    # PAYMENT METHOD
    # ========================================================

    PAYMENT_COD = "cod"
    PAYMENT_CARD = "card"
    PAYMENT_ONLINE = "online"

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_COD, "Cash on Delivery"),
        (PAYMENT_CARD, "Card"),
        (PAYMENT_ONLINE, "Online Payment"),
    ]

    # ========================================================
    # BASIC ORDER INFORMATION
    # ========================================================

    order_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    # ========================================================
    # PAYMENT INFORMATION
    # ========================================================

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_PENDING,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_COD,
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    # ========================================================
    # PRICE INFORMATION
    # ========================================================

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    shipping_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # ========================================================
    # SHIPPING ADDRESS SNAPSHOT
    # ========================================================
    #
    # We intentionally store the address as text.
    #
    # Why?
    # If the customer changes/deletes their Address later,
    # the old order must still contain the original shipping
    # information.
    #

    shipping_full_name = models.CharField(
        max_length=150,
    )

    shipping_phone = models.CharField(
        max_length=30,
    )

    shipping_address_line_1 = models.CharField(
        max_length=255,
    )

    shipping_address_line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    shipping_city = models.CharField(
        max_length=100,
    )

    shipping_province = models.CharField(
        max_length=100,
    )

    shipping_postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    shipping_country = models.CharField(
        max_length=100,
        default="Pakistan",
    )

    # ========================================================
    # CUSTOMER NOTES
    # ========================================================

    notes = models.TextField(
        blank=True,
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

    # ========================================================
    # SPECIAL TIMESTAMPS
    # ========================================================

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    shipped_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    delivered_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    cancelled_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["user", "-created_at"],
            ),
            models.Index(
                fields=["status"],
            ),
            models.Index(
                fields=["payment_status"],
            ),
            models.Index(
                fields=["order_number"],
            ),
        ]

    def __str__(self):
        return f"{self.order_number} - {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()

        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        """
        Generates a unique order number such as:

        ZEV-20260824-482731
        """

        import random

        while True:
            timestamp = timezone.now().strftime("%Y%m%d")
            random_number = random.randint(100000, 999999)

            order_number = (
                f"ZEV-{timestamp}-{random_number}"
            )

            if not Order.objects.filter(
                order_number=order_number
            ).exists():
                return order_number


class OrderItem(models.Model):
    # ========================================================
    # RELATION
    # ========================================================

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    # ========================================================
    # PRODUCT SNAPSHOT
    # ========================================================
    #
    # We save these values at the time of purchase.
    #
    # If product name/SKU/price changes later,
    # old orders remain historically accurate.
    #

    product_name = models.CharField(
        max_length=200,
    )

    product_sku = models.CharField(
        max_length=100,
    )

    # ========================================================
    # PRICE
    # ========================================================

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # ========================================================
    # TIMESTAMP
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.product_name} "
            f"x {self.quantity}"
        )

    def save(self, *args, **kwargs):
        self.subtotal = (
            self.unit_price * self.quantity
        )

        super().save(*args, **kwargs)