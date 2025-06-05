from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from account.models import User
from product.models import Category, Product, CartItem


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
        exclude = ('description',)


class CartSerializer(serializers.Serializer):
    item_counts = serializers.IntegerField(default=0)
    total_price = serializers.FloatField(default=0.0)


class CartItemRequestBodySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate(self, attrs):
        product_id = attrs['product_id']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound(f'Product with id {product_id} not found!')

        quantity = attrs['quantity']
        if quantity > product.quantity or quantity < 1:
            raise ValidationError(f'Invalid quantity {quantity}')

        attrs['product'] = product

        return attrs


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'cart_id', 'quantity']
