from rest_framework import serializers

from .models import *


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "product_name",
            "product_sku",
            "quantity",
            "unit_price",
            "subtotal",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "product_name",
            "product_sku",
            "unit_price",
            "subtotal",
            "created_at",
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order

        fields = [
            "id",
            "order_number",
            "user",

            "status",

            "payment_status",
            "payment_method",
            "transaction_id",

            "subtotal",
            "discount",
            "shipping_fee",
            "tax",
            "total",

            "shipping_full_name",
            "shipping_phone",
            "shipping_address_line_1",
            "shipping_address_line_2",
            "shipping_city",
            "shipping_province",
            "shipping_postal_code",
            "shipping_country",

            "notes",

            "paid_at",
            "shipped_at",
            "delivered_at",
            "cancelled_at",

            "items",
            "total_items",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "order_number",
            "user",

            "status",

            "payment_status",
            "transaction_id",

            "subtotal",
            "discount",
            "shipping_fee",
            "tax",
            "total",

            "paid_at",
            "shipped_at",
            "delivered_at",
            "cancelled_at",

            "items",
            "total_items",

            "created_at",
            "updated_at",
        ]

    def get_total_items(self, obj):
        return sum(
            item.quantity
            for item in obj.items.all()
        )


class OrderListSerializer(serializers.ModelSerializer):

    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order

        fields = [
            "id",
            "order_number",
            "status",
            "payment_method",
            "payment_status",
            "subtotal",
            "shipping_fee",
            "tax",
            "discount",
            "total",
            "total_items",
            "created_at",
        ]

        read_only_fields = fields

    def get_total_items(self, obj):
        return sum(
            item.quantity
            for item in obj.items.all()
        )