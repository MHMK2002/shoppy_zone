# Generated by Django 4.2 on 2025-05-16 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_unit'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_products',
            field=models.ManyToManyField(to='product.product'),
        ),
    ]
