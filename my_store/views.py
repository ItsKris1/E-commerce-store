from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductCreateForm



class ProductsListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        categories = Category.objects.all()
        context['categories'] = categories

        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CreateProductView(CreateView):
    template_name = 'create_product.html'
    form_class = ProductCreateForm
    model = Product
    # fields = '__all__'
    success_url = reverse_lazy('products')


class ProductDetailsView(DetailView):
    template_name = 'product_details.html'
    model = Product
    context_object_name = 'products'


class ProductDeleteView(DeleteView):
    template_name = 'product_confirm_delete.html'
    model = Product
    success_url = reverse_lazy('products')
    context_object_name = 'products'


class ProductUpdateView(UpdateView):

    def get_success_url(self):
        return reverse_lazy('product_details', args=(self.object.id,))

    template_name = 'update_product.html'
    model = Product
    form_class = ProductCreateForm
    context_object_name = 'products'
