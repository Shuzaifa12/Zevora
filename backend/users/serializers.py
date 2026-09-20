


from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import (
    Address,
    Profile,
    User,
)


# ============================================================
# REGISTER
# ============================================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    password_confirm = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User

        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "password",
            "password_confirm",
        ]

    # --------------------------------------------------------
    # EMAIL VALIDATION
    # --------------------------------------------------------

    def validate_email(self, value):

        email = value.lower().strip()

        if User.objects.filter(
            email=email
        ).exists():

            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return email

    # --------------------------------------------------------
    # PASSWORD VALIDATION
    # --------------------------------------------------------

    def validate(self, attrs):

        if (
            attrs["password"]
            != attrs["password_confirm"]
        ):

            raise serializers.ValidationError(
                {
                    "password_confirm":
                        "Passwords do not match."
                }
            )

        return attrs

    # --------------------------------------------------------
    # CREATE USER
    # --------------------------------------------------------

    def create(self, validated_data):

        validated_data.pop(
            "password_confirm"
        )

        password = validated_data.pop(
            "password"
        )

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        user.is_email_verified = False

        user.save(
            update_fields=[
                "is_email_verified"
            ]
        )

        return user


# ============================================================
# LOGIN
# ============================================================

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):

        email = attrs["email"].lower().strip()

        password = attrs["password"]

        user = authenticate(
            username=email,
            password=password,
        )

        if user is None:

            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:

            raise serializers.ValidationError(
                "Your account is inactive."
            )

        if not user.is_email_verified: # type: ignore

            raise serializers.ValidationError(
                "Please verify your email before logging in."
            )

        attrs["user"] = user

        return attrs


# ============================================================
# USER
# ============================================================

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "is_email_verified",
            "date_joined",
        ]

        read_only_fields = [
            "id",
            "email",
            "is_email_verified",
            "date_joined",
        ]


# ============================================================
# PROFILE
# ============================================================

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile

        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
        ]


# ============================================================
# FORGOT PASSWORD
# ============================================================

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        return value.lower().strip()


# ============================================================
# RESET PASSWORD
# ============================================================

class ResetPasswordSerializer(serializers.Serializer):

    token = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    password_confirm = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):

        if (
            attrs["password"]
            != attrs["password_confirm"]
        ):

            raise serializers.ValidationError(
                {
                    "password_confirm":
                        "Passwords do not match."
                }
            )

        return attrs


# ============================================================
# ADDRESS
# ============================================================

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address

        fields = [
            "id",
            "address_type",
            "full_name",
            "phone",
            "address_line_1",
            "address_line_2",
            "city",
            "province",
            "postal_code",
            "country",
            "is_default",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]