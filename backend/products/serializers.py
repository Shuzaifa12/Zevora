# from rest_framework import serializers

# from .models import *

# from django.db.models import Avg


# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = [
#             "id",
#             "image",
#             "alt_text",
#             "is_primary",
#             "display_order",
#         ]


# class ProductVariantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductVariant
#         fields = [
#             "id",
#             "name",
#             "sku",
#             "price",
#             "sale_price",
#             "stock_quantity",
#             "is_active",
#         ]


# class ProductAttributeSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(
#         source="attribute.name",
#         read_only=True,
#     )

#     class Meta:
#         model = ProductAttribute
#         fields = [
#             "id",
#             "name",
#             "value",
#         ]


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = [
#             "id",
#             "name",
#             "slug",
#             "description",
#             "image",
#             "is_active",
#             "is_featured",
#         ]


# class SubCategorySerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(
#         source="category.name",
#         read_only=True,
#     )

#     class Meta:
#         model = SubCategory
#         fields = [
#             "id",
#             "name",
#             "slug",
#             "description",
#             "image",
#             "category",
#             "category_name",
#             "is_active",
#         ]


# class BrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Brand
#         fields = [
#             "id",
#             "name",
#             "slug",
#             "description",
#             "logo",
#             "is_active",
#         ]


# class AttributeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attribute
#         fields = [
#             "id",
#             "name",
#             "slug",
#             "is_active",
#         ]


# class ProductSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(
#         source="category.name",
#         read_only=True,
#     )

#     subcategory_name = serializers.CharField(
#         source="subcategory.name",
#         read_only=True,
#     )

#     brand_name = serializers.CharField(
#         source="brand.name",
#         read_only=True,
#     )

#     images = ProductImageSerializer(
#         many=True,
#         read_only=True,
#     )

#     variants = ProductVariantSerializer(
#         many=True,
#         read_only=True,
#     )

#     attributes = ProductAttributeSerializer(
#         many=True,
#         read_only=True,
#     )

#     current_price = serializers.ReadOnlyField()
#     discount_percentage = serializers.ReadOnlyField()
#     average_rating = serializers.SerializerMethodField()
#     review_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "name",
#             "slug",
#             "sku",

#             "category",
#             "category_name",

#             "subcategory",
#             "subcategory_name",

#             "brand",
#             "brand_name",

#             "short_description",
#             "description",

#             "price",
#             "sale_price",
#             "current_price",
#             "discount_percentage",

#             "is_active",
#             "is_featured",
#             "is_new",
#             "is_bestseller",
#             "is_trending",

#             "images",
#             "variants",
#             "attributes",

#             "created_at",
#             "updated_at",

#             "average_rating",
#             "review_count",
#         ]

# def get_average_rating(self, obj):
#     result = obj.reviews.filter(
#         is_approved=True,
#         is_active=True,
#     ).aggregate(
#         average=Avg("rating")
#     )

#     return round(result["average"] or 0, 2)


# def get_review_count(self, obj):
#     return obj.reviews.filter(
#         is_approved=True,
#         is_active=True,
#     ).count()


# class WishlistSerializer(serializers.ModelSerializer):

#     product_name = serializers.CharField(
#         source="product.name",
#         read_only=True,
#     )

#     product_price = serializers.DecimalField(
#         source="product.price",
#         max_digits=10,
#         decimal_places=2,
#         read_only=True,
#     )

#     product_image = serializers.ImageField(
#         source="product.image",
#         read_only=True,
#     )

#     class Meta:
#         model = Wishlist

#         fields = [
#             "id",
#             "product",
#             "product_name",
#             "product_price",
#             "product_image",
#             "created_at",
#         ]

#         read_only_fields = [
#             "id",
#             "product_name",
#             "product_price",
#             "product_image",
#             "created_at",
#         ]

# class CartItemSerializer(serializers.ModelSerializer):

#     product_name = serializers.CharField(
#         source="product.name",
#         read_only=True,
#     )

#     product_price = serializers.DecimalField(
#         source="product.price",
#         max_digits=10,
#         decimal_places=2,
#         read_only=True,
#     )

#     subtotal = serializers.SerializerMethodField()

#     class Meta:
#         model = CartItem

#         fields = [
#             "id",
#             "product",
#             "product_name",
#             "product_price",
#             "quantity",
#             "unit_price",
#             "subtotal",
#         ]

#         read_only_fields = [
#             "id",
#             "product_name",
#             "product_price",
#             "unit_price",
#             "subtotal",
#         ]

#     def get_subtotal(self, obj):
#         return obj.subtotal

# class CartSerializer(serializers.ModelSerializer):

#     items = CartItemSerializer(
#         many=True,
#         read_only=True,
#     )

#     total_items = serializers.IntegerField(
#         read_only=True,
#     )

#     subtotal = serializers.SerializerMethodField()

#     class Meta:
#         model = Cart

#         fields = [
#             "id",
#             "items",
#             "total_items",
#             "subtotal",
#             "created_at",
#             "updated_at",
#         ]

#         read_only_fields = [
#             "id",
#             "items",
#             "total_items",
#             "subtotal",
#             "created_at",
#             "updated_at",
#         ]

#     def get_subtotal(self, obj):
#         return obj.subtotal

from django.db.models import Avg
from rest_framework import serializers

from .models import (
    Attribute,
    Brand,
    Cart,
    CartItem,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
    ProductVariant,
    SubCategory,
    Wishlist,
)


# ============================================================
# PRODUCT IMAGE
# ============================================================

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = [
            "id",
            "image",
            "alt_text",
            "is_primary",
            "display_order",
        ]


# ============================================================
# PRODUCT VARIANT
# ============================================================

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant

        fields = [
            "id",
            "name",
            "sku",
            "price",
            "sale_price",
            "stock_quantity",
            "is_active",
        ]


# ============================================================
# PRODUCT ATTRIBUTE
# ============================================================

class ProductAttributeSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        source="attribute.name",
        read_only=True,
    )

    class Meta:
        model = ProductAttribute

        fields = [
            "id",
            "name",
            "value",
        ]

        read_only_fields = [
            "id",
            "name",
        ]


# ============================================================
# CATEGORY
# ============================================================

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "is_active",
            "is_featured",
        ]


# ============================================================
# SUB CATEGORY
# ============================================================

class SubCategorySerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = SubCategory

        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "category",
            "category_name",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "category_name",
        ]


# ============================================================
# BRAND
# ============================================================

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand

        fields = [
            "id",
            "name",
            "slug",
            "description",
            "logo",
            "is_active",
        ]


# ============================================================
# ATTRIBUTE
# ============================================================

class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute

        fields = [
            "id",
            "name",
            "slug",
            "is_active",
        ]


# ============================================================
# PRODUCT
# ============================================================

class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True,
    )

    brand_name = serializers.CharField(
        source="brand.name",
        read_only=True,
    )

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True,
    )

    attributes = ProductAttributeSerializer(
        many=True,
        read_only=True,
    )

    current_price = serializers.ReadOnlyField()

    discount_percentage = serializers.ReadOnlyField()

    average_rating = serializers.SerializerMethodField()

    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = [
            # Basic
            "id",
            "name",
            "slug",
            "sku",

            # Relationships
            "category",
            "category_name",

            "subcategory",
            "subcategory_name",

            "brand",
            "brand_name",

            # Description
            "short_description",
            "description",

            # Pricing
            "price",
            "sale_price",
            "current_price",
            "discount_percentage",
            "stock",

            # Status
            "is_active",
            "is_featured",
            "is_new",
            "is_bestseller",
            "is_trending",

            # Related data
            "images",
            "variants",
            "attributes",

            # Dates
            "created_at",
            "updated_at",

            # Reviews
            "average_rating",
            "review_count",
        ]

        read_only_fields = [
            "id",
            "category_name",
            "subcategory_name",
            "brand_name",
            "current_price",
            "discount_percentage",
            "images",
            "variants",
            "attributes",
            "created_at",
            "updated_at",
            "average_rating",
            "review_count",
        ]

    # --------------------------------------------------------
    # AVERAGE RATING
    # --------------------------------------------------------

    def get_average_rating(self, obj):

        result = obj.reviews.filter(
            is_approved=True,
            is_active=True,
        ).aggregate(
            average=Avg("rating")
        )

        average = result.get("average")

        if average is None:
            return 0

        return round(float(average), 2)

    # --------------------------------------------------------
    # REVIEW COUNT
    # --------------------------------------------------------

    def get_review_count(self, obj):

        return obj.reviews.filter(
            is_approved=True,
            is_active=True,
        ).count()


# ============================================================
# WISHLIST
# ============================================================

class WishlistSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist

        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "product_image",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "product_name",
            "product_price",
            "product_image",
            "created_at",
        ]

    # --------------------------------------------------------
    # PRODUCT IMAGE
    # --------------------------------------------------------

    def get_product_image(self, obj):

        product = obj.product

        image = (
            product.images
            .filter(is_primary=True)
            .first()
        )

        if image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    image.image.url
                )

            return image.image.url

        image = (
            product.images
            .order_by("display_order")
            .first()
        )

        if image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    image.image.url
                )

            return image.image.url

        return None


# ============================================================
# CART ITEM
# ============================================================

class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem

        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "unit_price",
            "subtotal",
        ]

        read_only_fields = [
            "id",
            "product_name",
            "product_price",
            "unit_price",
            "subtotal",
        ]

    # --------------------------------------------------------
    # SUBTOTAL
    # --------------------------------------------------------

    def get_subtotal(self, obj):

        return obj.subtotal


# ============================================================
# CART
# ============================================================

class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        source="cart_items",
        many=True,
        read_only=True,
    )

    total_items = serializers.IntegerField(
        read_only=True,
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart

        fields = [
            "id",
            "items",
            "total_items",
            "subtotal",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "items",
            "total_items",
            "subtotal",
            "created_at",
            "updated_at",
        ]

    # --------------------------------------------------------
    # CART SUBTOTAL
    # --------------------------------------------------------

    def get_subtotal(self, obj):

        return obj.subtotal