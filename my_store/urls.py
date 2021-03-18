from django.urls import path
from . import views

urlpatterns = [
    path('products_list', views.ProductsListView.as_view(), name='products'),
    path('categories_list', views.CategoryListView.as_view(), name='categories'),
    path('create_product', views.CreateProductView.as_view(), name='create_product'),
]

