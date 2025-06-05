from django.db import models
from django.db.models import Q

from product.enums import ProductUnitEnum, CartStatusEnum


class Category(models.Model):
    title = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='category/')
    description = models.TextField()

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='product/')
    price = models.PositiveBigIntegerField()
    unit = models.CharField(max_length=128, choices=ProductUnitEnum.choices)
    quantity = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    rate_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(to='account.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=128, choices=CartStatusEnum.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'status'],
                condition=Q(status=CartStatusEnum.OPEN),
                name='unique_open_cart_per_user',
            )
        ]


class CartItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['product', 'cart'], name='cart_item_unique')]
