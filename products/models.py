import time

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from ckeditor.fields import RichTextField

from media.models import Media
from config import settings


# Create your models here.

class Category(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=120, unique=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=120, unique=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=120, unique=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Tags')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.title


class Products(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=120)
    price = models.IntegerField(verbose_name=_('Price'), default=0)
    images = models.ManyToManyField(Media, verbose_name=_('Images'))
    short_description = models.CharField(verbose_name=_('Short description'), max_length=150)
    size = models.ForeignKey(Size, verbose_name=_('Size'), on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_('Quantity'), default=0)
    sku = models.CharField(max_length=255, unique=True, blank=True, null=True)
    tags = models.ManyToManyField(Tags, verbose_name=_('Tags'))
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE)
    description = RichTextField(verbose_name=_('Description'))
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    looked = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ProductsReactions', related_name='product')

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = str(int(time.time() * 1000))
        super().save(*args, **kwargs)  # Сохранение модели для получения ID

    # Этот метод возвращает базовый URL продукта, который используется в методах для генерации социальных ссылок
    def get_absolute_url(self):
        # Вместо example.com укажите свой адрес сайта и домен
        return f"http://example.com/products/{self.id}/"

    # Ссылка для facebook
    def get_share_url_facebook(self):
        base_url = self.get_absolute_url()
        return f"https://www.facebook.com/sharer/sharer.php?u={base_url}"

    # Ссылка для twitter
    def get_share_url_twitter(self):
        base_url = self.get_absolute_url()
        tweet_text = f"Check out this product: {self.title}"
        return f"https://twitter.com/intent/tweet?url={base_url}&text={tweet_text}"

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return f"{self.title} - SKU: {self.sku}"


class ProductsReactions(models.Model):
    Rating_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name=_('Product'), on_delete=models.CASCADE,
                                related_name='product_reaction')
    is_liked = models.BooleanField(verbose_name=_('Liked'), default=False)
    rating = models.PositiveSmallIntegerField(choices=Rating_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = _('Product Reaction')
        verbose_name_plural = _('Products Reactions')

    def __str__(self):
        return f'{self.user.username} - {self.product.title}'


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name=_("User"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def get_total_price(self):
        total = sum(item.total_price for item in self.cart_items.all())
        return total

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"Cart for user {self.user.username if self.user else 'Guest'}"


class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_("Product"))
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE, verbose_name=_("Cart"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))

    def save(self, *args, **kwargs):
        if not self.pk:  # Проверяем, что объект новый
            self.quantity = self.product.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} (in cart {self.cart.id})"

    @property
    def total_price(self):
        return self.quantity * self.product.price


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Users")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Products")
    comment = models.TextField(verbose_name="Comments")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.title}"
