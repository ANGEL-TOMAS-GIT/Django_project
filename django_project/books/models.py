from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class ActiveProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True, stock__gt=0)


class Book(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="books"
    )
    title = models.CharField(_("Book Title"), max_length=40)
    slug = models.SlugField(unique=True)
    book_author = models.CharField(_("Book author"), max_length=30, blank=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="images/", blank=True, null=True)

    objects = models.Manager()
    active = ActiveProductManager()

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(stock__gte=0),
                name="non_negative_stock"
            )
        ]

    def __str__(self) -> str:
        return f'{self.title}({self.created_at}) - {self.author}'

    @property
    def current_price(self) -> bool:
        return self.discount_price or self.price

    DEFAULT_IMAGE = "/static/default_image.svg"

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return self.DEFAULT_IMAGE


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.user.email
