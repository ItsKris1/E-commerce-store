from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductCreateForm, CategoryCreateForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.core.exceptions import ObjectDoesNotExist

# Products
class ProductsListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'


    def get_queryset(self):
        products = Product.objects.all()

        category_id = self.request.GET.get('category', None)
        search = self.request.GET.get('search', None)

        if search is not None:
            products = products.filter(name__icontains=search)

        if category_id is not None:
            products = products.filter(category__id=int(category_id))

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        categories = Category.objects.all()
        context['categories'] = categories

        category_id = self.request.GET.get('category', None)
        try:
            category_name = Category.objects.get(pk=category_id)
        except ObjectDoesNotExist:
            category_name = None

        context['category_name'] = category_name

        return context


class CreateProductView(CreateView, PermissionRequiredMixin):
    permission_required = ['my_store.add_product']
    template_name = 'create_product.html'
    form_class = ProductCreateForm
    model = Product
    # fields = '__all__'
    success_url = reverse_lazy('products')


class ProductDetailsView(DetailView):
    template_name = 'product_details.html'
    model = Product
    context_object_name = 'products'


class ProductDeleteView(DeleteView, PermissionRequiredMixin):
    permission_required = ['my_store.delete_product']

    template_name = 'product_confirm_delete.html'
    model = Product
    success_url = reverse_lazy('products')
    context_object_name = 'products'


class ProductUpdateView(UpdateView, PermissionRequiredMixin):
    permission_required = ['my_store.change_product']

    def get_success_url(self):
        return reverse_lazy('product_details', args=(self.object.id,))

    template_name = 'update_product.html'
    model = Product
    form_class = ProductCreateForm
    context_object_name = 'products'


class ProductBuyView(TemplateView):
    template_name = 'buy_product.html'

    def get_context_data(self, pk, **kwargs):
        product = Product.objects.get(id=pk)

        product.quantity = product.quantity - 1
        product.save()

        context = super().get_context_data(**kwargs)
        context['product'] = product

        return context


# Categories
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CreateCategoryView(CreateView, PermissionRequiredMixin):
    permission_required = ['my_store.create_category']

    template_name = 'create_category.html'
    form_class = CategoryCreateForm
    model = Category
    # fields = '__all__'
    success_url = reverse_lazy('categories')


class CategoryDeleteView(DeleteView, PermissionRequiredMixin):
    permission_required = ['my_store.delete_category']

    template_name = 'category_confirm_delete.html'
    model = Category
    success_url = reverse_lazy('categories')
    context_object_name = 'categories1'


class CategoryUpdateView(UpdateView):
    template_name = 'edit_category.html'
    model = Category
    context_object_name = 'categories1'
    fields = '__all__'

# LOGIN
class Logout(LogoutView):
    next_page = 'products'

