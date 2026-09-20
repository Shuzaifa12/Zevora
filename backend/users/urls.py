from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(
    "addresses",
    AddressViewSet,
    basename="address",
)

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "verify-email/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),

    path(
        "resend-verification/",
        ResendVerificationView.as_view(),
        name="resend-verification",
    ),

    path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot-password",
    ),

    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),

    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]

urlpatterns += router.urls