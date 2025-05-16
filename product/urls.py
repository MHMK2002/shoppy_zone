from django.urls import path

from product.views import CategoriesView, ProductListView, FavoriteProductListView, FavoriteProductDetailView

urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/favorites/', FavoriteProductListView.as_view()),
    path('products/favorites/<str:product_id>/', FavoriteProductDetailView.as_view()),
]
