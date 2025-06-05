from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from product.enums import CartStatusEnum
from product.models import Category, Product, Cart, CartItem
from product.serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemRequestBodySerializer, \
    CartItemSerializer


class CategoriesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'


class ProductListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    ordering_fields = ('price',)
    filterset_fields = ['category_id']
    search_fields = ['title', 'slug']
    queryset = Product.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class FavoriteProductListView(ProductListView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(user=user)


class FavoriteProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, product_id: int) -> Response:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.favorite_products.filter(id=product_id).exists():
            return Response({'message': 'Product already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.favorite_products.add(product)

        return Response({'message': 'OK'})

    def delete(self, request: Request, product_id: int) -> Response:
        if product := request.user.favorite_products.filter(id=product_id).first():
            request.user.favorite_products.remove(product)
            return Response({'message': 'OK'})
        else:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        # TODO: N+1 Query warning. Fix me later.
        try:
            cart = Cart.objects.get(user=request.user, status=CartStatusEnum.OPEN)
        except Cart.DoesNotExist:
            serializer = CartSerializer()
            return Response(serializer.data)

        total_price = 0.0
        item_counts = 0

        for item in cart.cartitem_set.all():
            item_counts += item.quantity
            total_price += item.quantity * item.product.price

        serializer = CartSerializer({'total_price': total_price, 'item_counts': item_counts})

        return Response(serializer.data)

    @transaction.atomic
    def put(self, request: Request) -> Response:
        serializer = CartItemRequestBodySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(user=request.user, status=CartStatusEnum.OPEN)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            product.quantity -= quantity
            product.quantity += cart_item.quantity
            product.save()
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
            product.quantity -= quantity
            product.save()

        result_serializer = CartItemSerializer(cart_item)
        return Response(result_serializer.data)
