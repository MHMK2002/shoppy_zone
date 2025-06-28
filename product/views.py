from django.db import transaction
from django.db.models import F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from product.enums import CartStatusEnum
from product.models import Category, Product, Cart, CartItem, Comment
from product.serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemRequestBodySerializer, \
    CartItemSerializer, CommentSerializer, UpdateProductsSerializer, CartItemDetailSerializer


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

    def get_queryset(self):
        queryset = Product.objects.all()

        if min_price := self.request.GET.get('min_price'):
            queryset = queryset.filter(price__gte=min_price)

        if max_price := self.request.GET.get('max_price'):
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class FavoriteProductListView(ProductListView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user)


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

        queryset = cart.cartitem_set.annotate(
            price=F('quantity') * F('product__price'),
        ).aggregate(
            total_price=Sum('price', default=0),
            item_counts=Sum('quantity', default=0),
        )

        serializer = CartSerializer(queryset)

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


class CartItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, cart_id: int) -> Response:
        cart = get_object_or_404(Cart.objects, user=request.user, id=cart_id)
        queryset = cart.cartitem_set.annotate(
            total_price=F('quantity') * F('product__price')
        )
        serializer = CartItemDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, product_id: int) -> Response:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            product=product,
            user=request.user,
            rate=serializer.validated_data['rate'],
            content=serializer.validated_data['content']
        )

        res_serializer = CommentSerializer(comment)
        return Response(res_serializer.data)

    def delete(self, request: Request, product_id: int) -> Response:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = Comment.objects.get(product=product, user=request.user)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminProductView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request: Request) -> Response:
        serializer = UpdateProductsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        product_ids = serializer.validated_data['product_ids']

        products = Product.objects.filter(id__in=product_ids)
        products.update(quantity=0)

        res_serializer = ProductSerializer(products, many=True, context={'user': request.user})
        return Response(res_serializer.data, status=status.HTTP_200_OK)
