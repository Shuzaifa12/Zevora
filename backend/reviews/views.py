from django.db.models import Avg

from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import ValidationError

from .models import *
from .serializers import *

from django_filters.rest_framework import DjangoFilterBackend  # type: ignore


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "product",
        "rating",
    ]

    ordering_fields = [
        "created_at",
        "rating",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        return (
            Review.objects
            .filter(
                is_approved=True,
                is_active=True,
            )
            .select_related(
                "user",
                "product",
            )
        )

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]

        existing_review = Review.objects.filter(
            product=product,
            user=self.request.user,
        ).exists()

        if existing_review:
            raise ValidationError(
                "You have already reviewed this product."
            )

        serializer.save(
            user=self.request.user,
        )

    def perform_update(self, serializer):
        serializer.save(
            is_approved=False,
        )