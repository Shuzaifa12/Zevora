# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth import logout
# from django.core.mail import send_mail

# from rest_framework import status, permissions, viewsets
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from rest_framework_simplejwt.tokens import RefreshToken

# from .emails import *

# from .serializers import *
# from .utils import *
# from .models import *




# # Create your views here.
# def Users(request):
#     return HttpResponse ("Welcome {user.username}")


# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(
#             data=request.data
#         )

#         serializer.is_valid(raise_exception=True)

#         user = serializer.save()

#         token = create_verification_token(user)

#         send_verification_email(
#             user,
#             token,
#         )

#         return Response(
#             {
#                 "message": (
#                     "Account created successfully. "
#                     "Please verify your email."
#                 ),
#                 "email": user.email,
#             },
#             status=status.HTTP_201_CREATED,
#         )

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(
#             data=request.data
#         )

#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data["user"]

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "message": "Login successful.",
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": UserSerializer(user).data,
#         })

# class VerifyEmailView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         token = request.data.get("token")

#         if not token:
#             return Response(
#                 {"error": "Verification token is required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             data = verify_verification_token(token)

#             user = User.objects.get(
#                 id=data["user_id"],
#                 email=data["email"],
#             )

#         except Exception:
#             return Response(
#                 {"error": "Invalid or expired verification token."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if user.is_email_verified:
#             return Response({
#                 "message": "Email is already verified."
#             })

#         user.is_email_verified = True

#         user.save(
#             update_fields=["is_email_verified"]
#         )

#         return Response({
#             "message": "Email verified successfully."
#         })

# class ResendVerificationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get("email")

#         if not email:
#             return Response(
#                 {"error": "Email is required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             user = User.objects.get(
#                 email=email.lower().strip()
#             )
#         except User.DoesNotExist:
#             return Response(
#                 {
#                     "message": (
#                         "If the account exists, "
#                         "a verification email has been sent."
#                     )
#                 }
#             )

#         if user.is_email_verified:
#             return Response({
#                 "message": "Email is already verified."
#             })

#         token = create_verification_token(user)

#         send_verification_email(
#             user,
#             token,
#         )

#         return Response({
#             "message": "Verification email sent."
#         })

# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(
#             UserSerializer(request.user).data
#         )

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         refresh_token = request.data.get("refresh")

#         if not refresh_token:
#             return Response(
#                 {"error": "Refresh token is required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response({
#                 "message": "Logout successful."
#             })

#         except Exception:
#             return Response(
#                 {"error": "Invalid refresh token."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

# class ForgotPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = ForgotPasswordSerializer(
#             data=request.data
#         )

#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data["email"] # type: ignore

#         try:
#             user = User.objects.get(
#                 email=email
#             )
#         except User.DoesNotExist:
#             return Response({
#                 "message": (
#                     "If an account with this email exists, "
#                     "a password reset email has been sent."
#                 )
#             })

#         if not user.is_active:
#             return Response({
#                 "message": (
#                     "If an account with this email exists, "
#                     "a password reset email has been sent."
#                 )
#             })

#         token = create_password_reset_token(user)

#         send_password_reset_email(
#             user,
#             token,
#         )

#         return Response({
#             "message": (
#                 "If an account with this email exists, "
#                 "a password reset email has been sent."
#             )
#         })

# class ResetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = ResetPasswordSerializer(
#             data=request.data
#         )

#         serializer.is_valid(raise_exception=True)

#         token = serializer.validated_data["token"] # type: ignore

#         try:
#             data = verify_password_reset_token(
#                 token
#             )

#             user = User.objects.get(
#                 id=data["user_id"],
#                 email=data["email"],
#             )

#         except Exception:
#             return Response(
#                 {
#                     "error": (
#                         "Invalid or expired "
#                         "password reset token."
#                     )
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if not user.is_active:
#             return Response(
#                 {
#                     "error": "This account is inactive."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         user.set_password(
#             serializer.validated_data["password"] # type: ignore
#         )

#         user.save(
#             update_fields=["password"]
#         )

#         return Response({
#             "message": (
#                 "Password reset successfully. "
#                 "You can now login with your new password."
#             )
#         })

# class ProfileView(APIView):

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def get(self, request):

#         profile, created = Profile.objects.get_or_create(
#             user=request.user
#         )

#         return Response(
#             UserSerializer(profile).data
#         )

#     def patch(self, request):

#         profile, created = Profile.objects.get_or_create(
#             user=request.user
#         )

#         serializer = UserSerializer(
#             profile,
#             data=request.data,
#             partial=True,
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         serializer.save()

#         return Response(
#             serializer.data
#         )

# class AddressViewSet(viewsets.ModelViewSet):

#     serializer_class = AddressSerializer

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def get_queryset(self):

#         return Address.objects.filter(
#             user=self.request.user
#         )

#     def perform_create(self, serializer):

#         serializer.save(
#             user=self.request.user
#         )


from django.http import HttpResponse

from rest_framework import (
    permissions,
    status,
    viewsets,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .emails import (
    send_password_reset_email,
    send_verification_email,
)
from .models import (
    Address,
    Profile,
    User,
)
from .serializers import (
    AddressSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    UserSerializer,
)
from .utils import (
    create_password_reset_token,
    create_verification_token,
    verify_password_reset_token,
    verify_verification_token,
)


# ============================================================
# BASIC USER PAGE
# ============================================================

def Users(request):
    return HttpResponse(
        "Welcome to ZEVORA Users API"
    )


# ============================================================
# REGISTER
# ============================================================

class RegisterView(APIView):

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        token = create_verification_token(
            user
        )

        send_verification_email(
            user,
            token,
        )

        return Response(
            {
                "message": (
                    "Account created "
                    "successfully. "
                    "Please verify "
                    "your email."
                ),
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# LOGIN
# ============================================================

class LoginView(APIView):

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data[
            "user"
        ]

        refresh = RefreshToken.for_user(
            user
        )

        return Response(
            {
                "message": (
                    "Login successful."
                ),
                "access": str(
                    refresh.access_token
                ),
                "refresh": str(
                    refresh
                ),
                "user": UserSerializer(
                    user
                ).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# VERIFY EMAIL
# ============================================================

class VerifyEmailView(APIView):

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        token = request.data.get(
            "token"
        )

        if not token:
            return Response(
                {
                    "error": (
                        "Verification token "
                        "is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            data = verify_verification_token(
                token
            )

            user = User.objects.get(
                id=data["user_id"],
                email=data["email"],
            )

        except (
            Exception,
        ):
            return Response(
                {
                    "error": (
                        "Invalid or expired "
                        "verification token."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_email_verified:
            return Response(
                {
                    "message": (
                        "Email is already "
                        "verified."
                    )
                },
                status=status.HTTP_200_OK,
            )

        user.is_email_verified = True

        user.save(
            update_fields=[
                "is_email_verified"
            ]
        )

        return Response(
            {
                "message": (
                    "Email verified "
                    "successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# RESEND VERIFICATION
# ============================================================

class ResendVerificationView(APIView):

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        email = request.data.get(
            "email"
        )

        if not email:
            return Response(
                {
                    "error": (
                        "Email is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = email.lower().strip()

        try:
            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "message": (
                        "If the account "
                        "exists, a "
                        "verification email "
                        "has been sent."
                    )
                },
                status=status.HTTP_200_OK,
            )

        if user.is_email_verified:

            return Response(
                {
                    "message": (
                        "Email is already "
                        "verified."
                    )
                },
                status=status.HTTP_200_OK,
            )

        token = create_verification_token(
            user
        )

        send_verification_email(
            user,
            token,
        )

        return Response(
            {
                "message": (
                    "Verification email "
                    "sent."
                )
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# CURRENT USER
# ============================================================

class MeView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        return Response(
            UserSerializer(
                request.user
            ).data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# LOGOUT
# ============================================================

class LogoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        refresh_token = request.data.get(
            "refresh"
        )

        if not refresh_token:
            return Response(
                {
                    "error": (
                        "Refresh token "
                        "is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            token = RefreshToken(
                refresh_token
            )

            token.blacklist()

            return Response(
                {
                    "message": (
                        "Logout successful."
                    )
                },
                status=status.HTTP_200_OK,
            )

        except Exception:

            return Response(
                {
                    "error": (
                        "Invalid refresh "
                        "token."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# ============================================================
# FORGOT PASSWORD
# ============================================================

class ForgotPasswordView(APIView):

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        serializer = (
            ForgotPasswordSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = (
            serializer.validated_data[
                "email"
            ]
        )

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "message": (
                        "If an account "
                        "with this email "
                        "exists, a password "
                        "reset email has "
                        "been sent."
                    )
                },
                status=status.HTTP_200_OK,
            )

        if not user.is_active:

            return Response(
                {
                    "message": (
                        "If an account "
                        "with this email "
                        "exists, a password "
                        "reset email has "
                        "been sent."
                    )
                },
                status=status.HTTP_200_OK,
            )

        token = (
            create_password_reset_token(
                user
            )
        )

        send_password_reset_email(
            user,
            token,
        )

        return Response(
            {
                "message": (
                    "If an account "
                    "with this email "
                    "exists, a password "
                    "reset email has "
                    "been sent."
                )
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# RESET PASSWORD
# ============================================================

class ResetPasswordView(APIView):

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        serializer = (
            ResetPasswordSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        token = (
            serializer.validated_data[
                "token"
            ]
        )

        try:

            data = (
                verify_password_reset_token(
                    token
                )
            )

            user = User.objects.get(
                id=data["user_id"],
                email=data["email"],
            )

        except Exception:

            return Response(
                {
                    "error": (
                        "Invalid or expired "
                        "password reset token."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_active:

            return Response(
                {
                    "error": (
                        "This account "
                        "is inactive."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(
            serializer.validated_data[
                "password"
            ]
        )

        user.save(
            update_fields=[
                "password"
            ]
        )

        return Response(
            {
                "message": (
                    "Password reset "
                    "successfully. "
                    "You can now login "
                    "with your new "
                    "password."
                )
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# PROFILE
# ============================================================

class ProfileView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # --------------------------------------------------------
    # GET PROFILE
    # --------------------------------------------------------

    def get(self, request):

        profile, _ = (
            Profile.objects
            .get_or_create(
                user=request.user
            )
        )

        serializer = ProfileSerializer(
            profile
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # --------------------------------------------------------
    # UPDATE PROFILE
    # --------------------------------------------------------

    def patch(self, request):

        profile, _ = (
            Profile.objects
            .get_or_create(
                user=request.user
            )
        )

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# ADDRESS
# ============================================================

class AddressViewSet(
    viewsets.ModelViewSet
):

    serializer_class = AddressSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return (
            Address.objects
            .filter(
                user=self.request.user
            )
        )

    def perform_create(
        self,
        serializer
    ):

        serializer.save(
            user=self.request.user
        )