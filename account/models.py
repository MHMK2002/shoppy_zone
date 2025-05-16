from django.contrib.auth.models import AbstractUser
from django.db import models

from product.models import Product


# Create your models here.

class User(AbstractUser):
    favorite_products = models.ManyToManyField(Product)

