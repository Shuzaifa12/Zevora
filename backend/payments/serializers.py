from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True,
    )

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = Payment

        fields = [
            "id",

            "order",
            "order_number",

            "user",
            "user_email",

            "provider",
            "status",

            "amount",
            "currency",

            "transaction_id",
            "provider_payment_id",

            "gateway_response",
            "failure_reason",

            "refunded_amount",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "order_number",
            "user_email",
            "status",
            "amount",
            "currency",
            "transaction_id",
            "provider_payment_id",
            "gateway_response",
            "failure_reason",
            "refunded_amount",
            "created_at",
            "updated_at",
        ]


class CreatePaymentSerializer(serializers.Serializer):

    order_id = serializers.IntegerField()

    provider = serializers.ChoiceField(
        choices=[
            (Payment.PROVIDER_COD, "Cash on Delivery"),
            (Payment.PROVIDER_ONLINE, "Online Payment"),
        ]
    )

    def validate_order_id(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "A valid order ID is required."
            )

        return value