from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AttributeViewSet,
    BrandViewSet,
    CartView,
    CategoryViewSet,
    ClearCartView,
    ProductViewSet,
    SubCategoryViewSet,
    WishlistView,
)


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


urlpatterns = [
    # =========================================================
    # CART
    # =========================================================

    path(
        "cart/",
        CartView.as_view(),
        name="cart",
    ),

    path(
        "cart/clear/",
        ClearCartView.as_view(),
        name="cart-clear",
    ),

    # =========================================================
    # WISHLIST
    # =========================================================

    path(
        "wishlist/",
        WishlistView.as_view(),
        name="wishlist",
    ),

    # =========================================================
    # PRODUCT ROUTER
    # =========================================================

    path(
        "",
        include(router.urls),
    ),
]