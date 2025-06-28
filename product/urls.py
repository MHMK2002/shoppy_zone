from django.urls import path

from product.views import CategoriesView, ProductListView, FavoriteProductListView, FavoriteProductDetailView, CartView, \
    CommentView, AdminProductView, CartItemListView

urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/favorites/', FavoriteProductListView.as_view()),
    path('products/favorites/<str:product_id>/', FavoriteProductDetailView.as_view()),
    path('products/cart/', CartView.as_view()),
    path('products/cart/<int:cart_id>/', CartItemListView.as_view()),
    path('products/<int:product_id>/comment/', CommentView.as_view()),
    path('admin/product/', AdminProductView.as_view()),
]
