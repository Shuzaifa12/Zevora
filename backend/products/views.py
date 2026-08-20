from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from .filters import ProductFilter

from .models import *

from .serializers import *

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.filter(is_active=True)
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attribute.objects.filter(is_active=True)
    serializer_class = AttributeSerializer
    permission_classes = [AllowAny]


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
