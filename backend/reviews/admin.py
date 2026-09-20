from django.contrib import admin

from .models import *


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "is_approved",
        "is_active",
        "is_verified_purchase",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_approved",
        "is_active",
        "is_verified_purchase",
        "created_at",
    )

    search_fields = (
        "product__name",
        "user__email",
        "title",
        "comment",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )