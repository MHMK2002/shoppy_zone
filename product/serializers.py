from rest_framework import serializers

from product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('description',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('description', )
