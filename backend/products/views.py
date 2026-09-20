from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend # type: ignore

from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductFilter
from .models import (
    Attribute,
    Brand,
    Cart,
    CartItem,
    Category,
    Product,
    SubCategory,
    Wishlist,
)
from .serializers import (
    AttributeSerializer,
    BrandSerializer,
    CartSerializer,
    CategorySerializer,
    ProductSerializer,
    SubCategorySerializer,
    WishlistSerializer,
)


# ============================================================
# CATEGORY
# ============================================================

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(
        is_active=True
    )

    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# ============================================================
# SUB CATEGORY
# ============================================================

class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.filter(
        is_active=True
    )

    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny]


# ============================================================
# BRAND
# ============================================================

class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(
        is_active=True
    )

    serializer_class = BrandSerializer
    permission_classes = [AllowAny]


# ============================================================
# ATTRIBUTE
# ============================================================

class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attribute.objects.filter(
        is_active=True
    )

    serializer_class = AttributeSerializer
    permission_classes = [AllowAny]


# ============================================================
# PRODUCT
# ============================================================

class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = (
        Product.objects
        .filter(is_active=True)
        .select_related(
            "category",
            "subcategory",
            "brand",
        )
        .prefetch_related(
            "images",
            "variants",
            "attributes__attribute",
        )
    )

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ProductFilter

    search_fields = [
        "name",
        "sku",
        "description",
        "short_description",
        "brand__name",
        "category__name",
        "subcategory__name",
    ]

    ordering_fields = [
        "name",
        "price",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]


# ============================================================
# WISHLIST
# ============================================================

class WishlistView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # --------------------------------------------------------
    # GET WISHLIST
    # --------------------------------------------------------

    def get(self, request):

        wishlist = (
            Wishlist.objects
            .filter(user=request.user)
            .select_related("product")
        )

        serializer = WishlistSerializer(
            wishlist,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # --------------------------------------------------------
    # ADD TO WISHLIST
    # --------------------------------------------------------

    def post(self, request):

        product_id = request.data.get(
            "product"
        )

        if not product_id:
            return Response(
                {
                    "error": "Product ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(
                id=product_id,
                is_active=True,
            )

        except Product.DoesNotExist:
            return Response(
                {
                    "error": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        wishlist, created = (
            Wishlist.objects.get_or_create(
                user=request.user,
                product=product,
            )
        )

        if not created:
            return Response(
                {
                    "message": (
                        "Product is already "
                        "in your wishlist."
                    )
                },
                status=status.HTTP_200_OK,
            )

        serializer = WishlistSerializer(
            wishlist
        )

        return Response(
            {
                "message": (
                    "Product added to wishlist."
                ),
                "wishlist": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    # --------------------------------------------------------
    # REMOVE FROM WISHLIST
    # --------------------------------------------------------

    def delete(self, request):

        product_id = request.data.get(
            "product"
        )

        if not product_id:
            return Response(
                {
                    "error": "Product ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_count, _ = (
            Wishlist.objects
            .filter(
                user=request.user,
                product_id=product_id,
            )
            .delete()
        )

        if deleted_count == 0:
            return Response(
                {
                    "error": (
                        "Product is not "
                        "in your wishlist."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "message": (
                    "Product removed "
                    "from wishlist."
                )
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# CART
# ============================================================

class CartView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # --------------------------------------------------------
    # GET / CREATE CART
    # --------------------------------------------------------

    def get_cart(self, user):

        cart, _ = Cart.objects.get_or_create(
            user=user
        )

        return cart

    # --------------------------------------------------------
    # GET CART
    # --------------------------------------------------------

    def get(self, request):

        cart = self.get_cart(
            request.user
        )

        serializer = CartSerializer(
            cart
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # --------------------------------------------------------
    # ADD PRODUCT TO CART
    # --------------------------------------------------------

    @transaction.atomic
    def post(self, request):

        product_id = request.data.get(
            "product"
        )

        quantity = request.data.get(
            "quantity",
            1,
        )

        # Validate product ID
        if not product_id:
            return Response(
                {
                    "error": (
                        "Product ID is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate quantity
        try:
            quantity = int(quantity)

        except (
            TypeError,
            ValueError,
        ):
            return Response(
                {
                    "error": (
                        "Quantity must be "
                        "a valid number."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:
            return Response(
                {
                    "error": (
                        "Quantity must be "
                        "at least 1."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get active product
        try:
            product = (
                Product.objects
                .select_for_update()
                .get(
                    id=product_id,
                    is_active=True,
                )
            )

        except Product.DoesNotExist:
            return Response(
                {
                    "error": (
                        "Product not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Stock validation
        if product.stock <= 0:
            return Response(
                {
                    "error": (
                        "This product is "
                        "currently out of stock."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity > product.stock:
            return Response(
                {
                    "error": (
                        f"Only {product.stock} "
                        "items are available."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get user's cart
        cart = self.get_cart(
            request.user
        )

        # Get or create cart item
        cart_item, created = (
            CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    "quantity": quantity,
                    "unit_price": product.current_price,
                },
            )
        )

        # Existing item
        if not created:

            new_quantity = (
                cart_item.quantity
                + quantity
            )

            if new_quantity > product.stock:
                return Response(
                    {
                        "error": (
                            f"Only {product.stock} "
                            "items are available. "
                            f"You already have "
                            f"{cart_item.quantity} "
                            "in your cart."
                        )
                    },
                    status=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                )

            cart_item.quantity = (
                new_quantity
            )

            # Keep original unit price
            cart_item.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

        serializer = CartSerializer(
            cart
        )

        return Response(
            {
                "message": (
                    "Product added to cart."
                ),
                "cart": serializer.data,
            },
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )

    # --------------------------------------------------------
    # UPDATE CART QUANTITY
    # --------------------------------------------------------

    @transaction.atomic
    def patch(self, request):

        product_id = request.data.get(
            "product"
        )

        quantity = request.data.get(
            "quantity"
        )

        if not product_id:
            return Response(
                {
                    "error": (
                        "Product ID is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity is None:
            return Response(
                {
                    "error": (
                        "Quantity is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(quantity)

        except (
            TypeError,
            ValueError,
        ):
            return Response(
                {
                    "error": (
                        "Quantity must be "
                        "a valid number."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:
            return Response(
                {
                    "error": (
                        "Quantity must be "
                        "at least 1."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = self.get_cart(
            request.user
        )

        try:
            cart_item = (
                CartItem.objects
                .select_related("product")
                .get(
                    cart=cart,
                    product_id=product_id,
                )
            )

        except CartItem.DoesNotExist:
            return Response(
                {
                    "error": (
                        "Product is not "
                        "in your cart."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        product = cart_item.product

        if not product.is_active:
            return Response(
                {
                    "error": (
                        "This product is "
                        "no longer available."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if product.stock <= 0:
            return Response(
                {
                    "error": (
                        "This product is "
                        "currently out of stock."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity > product.stock:
            return Response(
                {
                    "error": (
                        f"Only {product.stock} "
                        "items are available."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item.quantity = quantity

        cart_item.save(
            update_fields=[
                "quantity",
                "updated_at",
            ]
        )

        serializer = CartSerializer(
            cart
        )

        return Response(
            {
                "message": "Cart updated.",
                "cart": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # --------------------------------------------------------
    # REMOVE PRODUCT FROM CART
    # --------------------------------------------------------

    @transaction.atomic
    def delete(self, request):

        product_id = request.data.get(
            "product"
        )

        if not product_id:
            return Response(
                {
                    "error": (
                        "Product ID is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = self.get_cart(
            request.user
        )

        deleted_count, _ = (
            CartItem.objects
            .filter(
                cart=cart,
                product_id=product_id,
            )
            .delete()
        )

        if deleted_count == 0:
            return Response(
                {
                    "error": (
                        "Product is not "
                        "in your cart."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CartSerializer(
            cart
        )

        return Response(
            {
                "message": (
                    "Product removed "
                    "from cart."
                ),
                "cart": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# CLEAR CART
# ============================================================

# class ClearCartView(APIView):

#     permission_classes = [
#         IsAuthenticated
#     ]

#     @transaction.atomic
#     def post(self, request):

#         cart, _ = (
#             Cart.objects.get_or_create(
#                 user=request.user
#             )
#         )

#         cart.cart_items.all().delete() # type: ignore

#         return Response(
#             {
#                 "message": (
#                     "Cart cleared successfully."
#                 )
#             },
#             status=status.HTTP_200_OK,
#         )

class ClearCartView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def delete(self, request):
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart.cart_items.all().delete() # type: ignore

        return Response(
            {
                "message": "Cart cleared successfully."
            },
            status=status.HTTP_200_OK,
        )