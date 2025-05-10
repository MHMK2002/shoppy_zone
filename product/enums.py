from django.db import models


class ProductUnitEnum(models.TextChoices):
    ONE_KG = '1kg', '1 KG'
    HALF_KG = '0.5kg', '0.5 KG'
    ONE = '1', '1'
