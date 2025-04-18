from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(max_length=128)
    image = models.ImageField(upload_to='product/')
    price = models.PositiveBigIntegerField()

