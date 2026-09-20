from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "category__name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "brand",
        "price",
        "sale_price",
        "is_active",
        "is_featured",
        "is_new",
        "is_bestseller",
    )

    list_filter = (
        "category",
        "brand",
        "is_active",
        "is_featured",
        "is_new",
        "is_bestseller",
        "is_trending",
    )

    search_fields = (
        "name",
        "sku",
        "brand__name",
        "category__name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [
        ProductImageInline,
        ProductVariantInline,
        ProductAttributeInline,
    ]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "is_primary",
        "display_order",
        "created_at",
    )

    list_filter = (
        "is_primary",
    )

    search_fields = (
        "product__name",
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "name",
        "sku",
        "price",
        "sale_price",
        "stock_quantity",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "product__name",
        "sku",
        "name",
    )

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "created_at",
    )

    search_fields = (
        "user__email",
        "product__name",
    )

    list_filter = (
        "created_at",
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "total_items",
        "subtotal",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart",
        "product",
        "quantity",
        "unit_price",
        "subtotal",
        "created_at",
    )

    search_fields = (
        "cart__user__email",
        "product__name",
    )

    list_filter = (
        "created_at",
    )