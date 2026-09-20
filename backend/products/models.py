from django.db import models
from django.conf import settings


# ============================================================
# CATEGORY
# ============================================================

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# ============================================================
# SUB CATEGORY
# ============================================================

class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )

    name = models.CharField(
        max_length=100,
    )

    slug = models.SlugField(
        max_length=120,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="subcategories/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

        constraints = [
            models.UniqueConstraint(
                fields=["category", "slug"],
                name="unique_subcategory_slug_per_category",
            )
        ]

    def __str__(self):
        return f"{self.category.name} → {self.name}"


# ============================================================
# BRAND
# ============================================================

class Brand(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    logo = models.ImageField(
        upload_to="brands/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# PRODUCT
# ============================================================

class Product(models.Model):

    name = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        related_name="products",
        blank=True,
        null=True,
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
    )

    short_description = models.CharField(
        max_length=500,
        blank=True,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    is_new = models.BooleanField(
        default=False,
    )

    is_bestseller = models.BooleanField(
        default=False,
    )

    is_trending = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["category"]
            ),
            models.Index(
                fields=["brand"]
            ),
            models.Index(
                fields=["is_active"]
            ),
            models.Index(
                fields=["is_featured"]
            ),
            models.Index(
                fields=["is_bestseller"]
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        if (
            self.sale_price is not None
            and self.sale_price < self.price
        ):
            return self.sale_price

        return self.price

    @property
    def discount_percentage(self):

        if (
            self.sale_price is None
            or self.price <= 0
            or self.sale_price >= self.price
        ):
            return 0

        discount = (
            (self.price - self.sale_price)
            / self.price
        ) * 100

        return round(discount, 2)


# ============================================================
# PRODUCT IMAGE
# ============================================================

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="products/",
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "display_order",
            "-created_at",
        ]

    def __str__(self):
        return f"{self.product.name} Image"


# ============================================================
# PRODUCT VARIANT
# ============================================================

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    name = models.CharField(
        max_length=100,
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    stock_quantity = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def current_price(self):

        if (
            self.sale_price is not None
            and self.sale_price < self.price # type: ignore
        ):
            return self.sale_price

        return self.price


# ============================================================
# ATTRIBUTE
# ============================================================

class Attribute(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# PRODUCT ATTRIBUTE
# ============================================================

class ProductAttribute(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="attributes",
    )

    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="product_values",
    )

    value = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["attribute__name"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product",
                    "attribute",
                ],
                name="unique_product_attribute",
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}"


# ============================================================
# WISHLIST
# ============================================================

class Wishlist(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "product",
                ],
                name="unique_user_product_wishlist",
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


# ============================================================
# CART
# ============================================================

class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Cart - {self.user.email}"

    @property
    def total_items(self):

        return sum(
            item.quantity
            for item in self.cart_items.all() # type: ignore
        )

    @property
    def subtotal(self):

        return sum(
            (
                item.subtotal
                for item in self.cart_items.all() # type: ignore
            ),
            0,
        )


# ============================================================
# CART ITEM
# ============================================================

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "cart",
                    "product",
                ],
                name="unique_cart_product",
            )
        ]

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return (
            f"{self.product.name} "
            f"x {self.quantity}"
        )