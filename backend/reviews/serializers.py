from rest_framework import serializers

from .models import *


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = Review

        fields = [
            "id",
            "product",
            "user",
            "user_name",
            "user_email",
            "rating",
            "title",
            "comment",
            "image",
            "is_verified_purchase",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "user",
            "user_name",
            "user_email",
            "is_verified_purchase",
            "created_at",
            "updated_at",
        ]

    def get_user_name(self, obj):
        full_name = obj.user.get_full_name()

        if full_name:
            return full_name

        return obj.user.username