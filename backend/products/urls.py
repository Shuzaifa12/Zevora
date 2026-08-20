from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()

router.register(
    r"categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    r"subcategories",
    SubCategoryViewSet,
    basename="subcategory",
)

router.register(
    r"brands",
    BrandViewSet,
    basename="brand",
)

router.register(
    r"attributes",
    AttributeViewSet,
    basename="attribute",
)

router.register(
    r"",
    ProductViewSet,
    basename="product",
)


urlpatterns = router.urls