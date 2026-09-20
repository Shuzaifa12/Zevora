from django.urls import path

from .views import (
    CreatePaymentView,
    PaymentDetailView,
    PaymentListView,
    MarkPaymentSuccessView,
    MarkPaymentFailedView
)


urlpatterns = [

    path(
        "create/",
        CreatePaymentView.as_view(),
        name="payment-create",
    ),

    path(
        "",
        PaymentListView.as_view(),
        name="payment-list",
    ),

    path(
        "<int:payment_id>/",
        PaymentDetailView.as_view(),
        name="payment-detail",
    ),

    path(
        "<int:payment_id>/success/",
        MarkPaymentSuccessView.as_view(),
        name="payment-success",
    ),

    path(
        "<int:payment_id>/failed/",
        MarkPaymentFailedView.as_view(),
        name="payment-failed",
    ),
]