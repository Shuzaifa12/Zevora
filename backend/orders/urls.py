# from django.urls import path

# from .views import (
#     CreateOrderView,
#     MyOrdersView,
#     OrderDetailView,
#     CancelOrderView,
# )


# urlpatterns = [
#     # Create COD Order
#     path(
#         "create/",
#         CreateOrderView.as_view(),
#         name="create-order",
#     ),

#     # Logged-in user's orders
#     path(
#         "my-orders/",
#         MyOrdersView.as_view(),
#         name="my-orders",
#     ),

#     # Single order detail
#     path(
#         "<int:pk>/",
#         OrderDetailView.as_view(),
#         name="order-detail",
#     ),

#     # Cancel order
#     path(
#         "<int:pk>/cancel/",
#         CancelOrderView.as_view(),
#         name="cancel-order",
#     ),
# ]

from django.urls import path

from .views import (
    CreateOrderView,
    MyOrdersView,
    OrderDetailView,
    CancelOrderView,
)


urlpatterns = [
    # Create order
    path(
        "create/",
        CreateOrderView.as_view(),
        name="create-order",
    ),

    # Logged-in user's orders
    path(
        "my-orders/",
        MyOrdersView.as_view(),
        name="my-orders",
    ),

    # Single order detail
    path(
        "<str:order_number>/",
        OrderDetailView.as_view(),
        name="order-detail",
    ),

    # Cancel order
    path(
        "<str:order_number>/cancel/",
        CancelOrderView.as_view(),
        name="cancel-order",
    ),
]