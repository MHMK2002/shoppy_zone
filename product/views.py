from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer


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
