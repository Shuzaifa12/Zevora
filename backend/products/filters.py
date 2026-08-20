import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
    )

    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
    )

    category = django_filters.NumberFilter(
        field_name="category_id",
    )

    subcategory = django_filters.NumberFilter(
        field_name="subcategory_id",
    )

    brand = django_filters.NumberFilter(
        field_name="brand_id",
    )

    is_featured = django_filters.BooleanFilter()

    is_new = django_filters.BooleanFilter()

    is_bestseller = django_filters.BooleanFilter()

    is_trending = django_filters.BooleanFilter()

    class Meta:
        model = Product

        fields = [
            "category",
            "subcategory",
            "brand",
            "is_featured",
            "is_new",
            "is_bestseller",
            "is_trending",
        ]