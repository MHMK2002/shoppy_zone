from rest_framework import serializers

from account.models import User
from product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('description',)


class ProductSerializer(serializers.ModelSerializer):
    is_user_favorite = serializers.SerializerMethodField()

    def get_is_user_favorite(self, obj: Product):
        # TODO: Bad way. Fix me later.
        user: User = self.context['user']

        if user.is_anonymous:
            return False

        return user.favorite_products.filter(id=obj.id).exists()


    class Meta:
        model = Product
        exclude = ('description', )
