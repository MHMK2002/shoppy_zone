from django.db import models

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
    unit = models.CharField(max_length=128)
    quantity = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    rate_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

