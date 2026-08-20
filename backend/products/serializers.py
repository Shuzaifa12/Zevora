from rest_framework import serializers

from .models import (
    Attribute,
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
    ProductVariant,
    SubCategory,
)


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


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = [
            "id",
            "name",
            "slug",
            "is_active",
        ]


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

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "sku",

            "category",
            "category_name",

            "subcategory",
            "subcategory_name",

            "brand",
            "brand_name",

            "short_description",
            "description",

            "price",
            "sale_price",
            "current_price",
            "discount_percentage",

            "is_active",
            "is_featured",
            "is_new",
            "is_bestseller",
            "is_trending",

            "images",
            "variants",
            "attributes",

            "created_at",
            "updated_at",
        ]