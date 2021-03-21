from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductCreateForm, CategoryCreateForm


# Products
class ProductsListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.all()

        category = self.request.GET.get('category', None)

        if category is not None:
            products = products.filter(category__id=int(category))

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        categories = Category.objects.all()
        context['categories'] = categories

        return context


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


# Categories
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class ElectronicsListView(ListView):
    model = Product
    template_name = 'category_electronics.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        categories = Category.objects.all()
        context['categories'] = categories

        return context


class ClothesListView(ListView):
    model = Product
    template_name = 'category_clothes.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        categories = Category.objects.all()
        context['categories'] = categories

        return context


class FruitsListView(ListView):
    model = Product
    template_name = 'category_fruits.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        categories = Category.objects.all()
        context['categories'] = categories

        return context


class CreateCategoryView(CreateView):
    template_name = 'create_category.html'
    form_class = CategoryCreateForm
    model = Category
    # fields = '__all__'
    success_url = reverse_lazy('categories')


class CategoryDeleteView(DeleteView):

    template_name = 'category_confirm_delete.html'
    model = Category
    success_url = reverse_lazy('categories')
    context_object_name = 'categories'

