from django.shortcuts import render
from .models import Product


def base_view(request):
    products = Product.objects.all()

    my_context = {
        'products': products,
    }
    return render(request, 'base.html', my_context)
