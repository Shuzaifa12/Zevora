from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_email_verified = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    avatar = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        blank=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )


    def __str__(self):
        return f"{self.user.email}'s Profile"




class Address(models.Model):

    ADDRESS_TYPES = [
        ("home", "Home"),
        ("office", "Office"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES,
        default="home",
    )

    full_name = models.CharField(
        max_length=150,
    )

    phone = models.CharField(
        max_length=30,
    )

    address_line_1 = models.CharField(
        max_length=255,
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
    )

    province = models.CharField(
        max_length=100,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="Pakistan",
    )

    is_default = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.city}"

    def save(self, *args, **kwargs):

        if self.is_default:
            Address.objects.filter(
                user=self.user,
                is_default=True,
            ).exclude(
                pk=self.pk
            ).update(
                is_default=False
            )

        super().save(*args, **kwargs)