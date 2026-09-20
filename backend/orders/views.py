from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Cart, CartItem, Product
from users.models import Address
from payments.services import PaymentService

from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderListSerializer,
)
from payments.models import Payment


# ============================================================
# CREATE ORDER / CHECKOUT
# ============================================================

class CreateOrderView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def post(self, request):

        user = request.user

        # ----------------------------------------------------
        # GET CART
        # ----------------------------------------------------

        try:
            cart = Cart.objects.prefetch_related(
                "cart_items__product"
            ).get(
                user=user
            )

        except Cart.DoesNotExist:
            return Response(
                {
                    "error": "Your cart is empty."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_items = list(
            cart.cart_items.select_related( # type: ignore
                "product"
            ).all()
        )

        if not cart_items:
            return Response(
                {
                    "error": "Your cart is empty."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # GET ADDRESS
        # ----------------------------------------------------

        address_id = request.data.get(
            "address_id"
        )

        if not address_id:
            return Response(
                {
                    "error": "Address ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            address = Address.objects.get(
                id=address_id,
                user=user,
            )

        except Address.DoesNotExist:
            return Response(
                {
                    "error": "Address not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ----------------------------------------------------
        # PAYMENT METHOD
        # ----------------------------------------------------

        payment_method = request.data.get(
            "payment_method",
            Order.PAYMENT_COD,
        )

        valid_payment_methods = {
            choice[0]
            for choice in Order.PAYMENT_METHOD_CHOICES
        }

        if payment_method not in valid_payment_methods:
            return Response(
                {
                    "error": "Invalid payment method.",
                    "allowed_methods": list(
                        valid_payment_methods
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # CUSTOMER NOTES
        # ----------------------------------------------------

        notes = request.data.get(
            "notes",
            "",
        )

        # ----------------------------------------------------
        # SHIPPING FEE
        # ----------------------------------------------------

        shipping_fee = Decimal(
            str(
                request.data.get(
                    "shipping_fee",
                    "0.00",
                )
            )
        )

        if shipping_fee < 0:
            return Response(
                {
                    "error": "Shipping fee cannot be negative."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # DISCOUNT
        # ----------------------------------------------------

        discount = Decimal(
            str(
                request.data.get(
                    "discount",
                    "0.00",
                )
            )
        )

        if discount < 0:
            return Response(
                {
                    "error": "Discount cannot be negative."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # STOCK CHECK + SUBTOTAL
        # ----------------------------------------------------

        subtotal = Decimal("0.00")

        for cart_item in cart_items:

            product = cart_item.product

            # Product must be active
            if not product.is_active:
                return Response(
                    {
                        "error": (
                            f"{product.name} "
                            "is currently unavailable."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Stock validation
            if cart_item.quantity > product.stock:
                return Response(
                    {
                        "error": (
                            f"Insufficient stock for "
                            f"{product.name}. "
                            f"Available stock: "
                            f"{product.stock}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use the current product price
            unit_price = product.current_price

            subtotal += (
                unit_price * cart_item.quantity
            )

        # ----------------------------------------------------
        # TAX
        # ----------------------------------------------------
        #
        # For now tax is 0.
        # We can add proper tax calculation later.
        #

        tax = Decimal("0.00")

        # ----------------------------------------------------
        # FINAL TOTAL
        # ----------------------------------------------------

        if discount > subtotal:
            return Response(
                {
                    "error": (
                        "Discount cannot be greater "
                        "than subtotal."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        total = (
            subtotal
            - discount
            + shipping_fee
            + tax
        )

        # ----------------------------------------------------
        # CREATE ORDER
        # ----------------------------------------------------

        order = Order.objects.create(
            user=user,

            status=Order.STATUS_PENDING,

            payment_method=payment_method,
            payment_status=Order.PAYMENT_PENDING,

            subtotal=subtotal,
            discount=discount,
            shipping_fee=shipping_fee,
            tax=tax,
            total=total,

            shipping_full_name=address.full_name,
            shipping_phone=address.phone,

            shipping_address_line_1=(
                address.address_line_1
            ),

            shipping_address_line_2=(
                address.address_line_2
            ),

            shipping_city=address.city,

            shipping_province=(
                address.province
            ),

            shipping_postal_code=(
                address.postal_code
            ),

            shipping_country=(
                address.country
            ),

            notes=notes,
        )

        # ----------------------------------------------------
        # CREATE ORDER ITEMS
        # ----------------------------------------------------

        for cart_item in cart_items:

            product = cart_item.product

            unit_price = product.current_price

            OrderItem.objects.create(
                order=order,

                product=product,

                product_name=product.name,

                product_sku=product.sku,

                unit_price=unit_price,

                quantity=cart_item.quantity,

            )

        # ----------------------------------------------------
        # REDUCE STOCK
        # ----------------------------------------------------

        for cart_item in cart_items:

            product = Product.objects.select_for_update().get(
                id=cart_item.product.id
            )

            product.stock -= cart_item.quantity

            product.save(
                update_fields=[
                    "stock",
                    "updated_at",
                ]
            )

        # ----------------------------------------------------
        # CREATE PAYMENT
        # ----------------------------------------------------

        try:

            payment = PaymentService.create_payment(
                user=user,
                order_id=order.id, # type: ignore
                provider=payment_method,
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # CLEAR CART
        # ----------------------------------------------------

        CartItem.objects.filter(
            cart=cart
        ).delete()

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        order_serializer = OrderSerializer(
            order
        )

        return Response(
            {
                "message": "Order created successfully.",
                "order": order_serializer.data,
                "payment": {
                    "id": payment.id, # type: ignore
                    "order_id": order.id, # type: ignore
                    "provider": payment.provider,
                    "status": payment.status,
                    "amount": str(payment.amount),
                    "currency": payment.currency,
                },
            },
            status=status.HTTP_201_CREATED,
        )

# ============================================================
# MY ORDERS
# ============================================================

class MyOrdersView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        orders = (
            Order.objects
            .filter(
                user=request.user
            )
            .prefetch_related(
                "items"
            )
        )

        serializer = OrderListSerializer(
            orders,
            many=True,
        )

        return Response(
            serializer.data
        )


# ============================================================
# ORDER DETAIL
# ============================================================

class OrderDetailView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, order_number):

        order = get_object_or_404(
            Order.objects.prefetch_related(
                "items"
            ),
            order_number=order_number,
            user=request.user,
        )

        serializer = OrderSerializer(
            order
        )

        return Response(
            serializer.data
        )


# ============================================================
# CANCEL ORDER
# ============================================================

class CancelOrderView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @transaction.atomic
    def post(self, request, order_number):

        order = get_object_or_404(
            Order.objects.select_for_update(),
            order_number=order_number,
            user=request.user,
        )

        # ----------------------------------------------------
        # CHECK ORDER STATUS
        # ----------------------------------------------------

        cancellable_statuses = [
            Order.STATUS_PENDING,
            Order.STATUS_CONFIRMED,
        ]

        if order.status not in cancellable_statuses:
            return Response(
                {
                    "error": (
                        "This order cannot be cancelled "
                        "at its current status."
                    ),
                    "current_status": order.status,
                    "payment_status": order.payment_status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------
        # RESTORE STOCK
        # ----------------------------------------------------

        order_items = order.items.select_related( # type: ignore
            "product"
        ).all()

        for item in order_items:

            product = Product.objects.select_for_update().get(
                id=item.product.id
            )

            product.stock += item.quantity

            product.save(
                update_fields=[
                    "stock",
                    "updated_at",
                ]
            )

        # ----------------------------------------------------
        # CANCEL RELATED PAYMENTS
        # ----------------------------------------------------

        payments = (
            Payment.objects
            .select_for_update()
            .filter(
                order=order,
                status__in=[
                    Payment.STATUS_PENDING,
                    Payment.STATUS_PROCESSING,
                ],
            )
        )

        for payment in payments:

            payment.status = Payment.STATUS_CANCELLED

            payment.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        # ----------------------------------------------------
        # CANCEL ORDER
        # ----------------------------------------------------

        order.status = Order.STATUS_CANCELLED
        order.payment_status = Order.PAYMENT_CANCELLED
        order.cancelled_at = timezone.now()

        order.save(
            update_fields=[
                "status",
                "payment_status",
                "cancelled_at",
                "updated_at",
            ]
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return Response(
            {
                "message": "Order cancelled successfully.",
                "order_number": order.order_number,
                "status": order.status,
                "payment_status": order.payment_status,
            },
            status=status.HTTP_200_OK,
        )

        