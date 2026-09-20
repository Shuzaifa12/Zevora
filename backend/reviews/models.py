from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.models import Product


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    title = models.CharField(
        max_length=200,
        blank=True,
    )

    comment = models.TextField()

    image = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True,
    )

    is_approved = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_verified_purchase = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"],
                name="unique_review_per_user_product",
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}/5)"