from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "order",
        "user",
        "provider",
        "status",
        "amount",
        "currency",
        "transaction_id",
        "created_at",
    ]

    list_filter = [
        "provider",
        "status",
        "currency",
        "created_at",
    ]

    search_fields = [
        "order__order_number",
        "user__email",
        "transaction_id",
        "provider_payment_id",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    ordering = [
        "-created_at",
    ]