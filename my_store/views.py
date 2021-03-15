from django.shortcuts import render
from django.views.generic import ListView
from .models import Product


class ProductsListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'


