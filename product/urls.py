from django.urls import path

from product.views import CategoriesView, ProductListView

urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('products/', ProductListView.as_view()),
]
