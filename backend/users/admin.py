from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
        "is_email_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "is_email_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )

    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
    )

    ordering = ("-date_joined",)

    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("Personal Information", {
            "fields": (
                "username",
                "first_name",
                "last_name",
                "phone",
            )
        }),
        ("Verification", {
            "fields": (
                "is_email_verified",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "password1",
                "password2",
            ),
        }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gender",
        "date_of_birth",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "full_name",
        "city",
        "province",
        "address_type",
        "is_default",
        "created_at",
    )

    list_filter = (
        "address_type",
        "is_default",
        "province",
        "city",
    )

    search_fields = (
        "user__email",
        "full_name",
        "phone",
        "city",
        "address_line_1",
    )