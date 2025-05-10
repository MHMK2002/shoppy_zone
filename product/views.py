from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
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
