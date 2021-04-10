from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView, View
from django.urls import reverse_lazy


from .models import Product, Category, Profile, OrderItem, Order, BillingAddress
from .forms import ProductCreateForm, CategoryCreateForm, SignUpForm, UserProfileUpdateForm, UserUpdateForm, CheckoutForm

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView


from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404


# Products
class ProductsListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.all()

        # SORT BY PRICE
        price = self.request.GET.get('price', None)

        if price == 'desc':
            products = products.order_by('-price')

        if price == 'asc':
            products = products.order_by('price')

        # -- SORT BY PRICE END --

        # SORT BY BRAND
        brand = self.request.GET.get('brand', None)

        if brand is not None:
            products = products.filter(brand__iexact=brand)

        # -- SORT BY BRAND END --

        # SORT BY SEARCH
        search = self.request.GET.get('search', None)

        if search is not None:
            products = products.filter(name__icontains=search)

        # -- SORT BY SEARCH END --

        # -- SORT BY CATEGORY
        category_id = self.request.GET.get('category', None)

        if category_id is not None:
            products = products.filter(category__id=int(category_id))

        # -- SORT BY CATEGORY END --

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        # CATEGORIES
        categories = Category.objects.all()
        context['categories'] = categories
        # --

        # CATEGORY NAME
        category_id = self.request.GET.get('category', None)
        try:
            category_name = Category.objects.get(pk=category_id)
        except ObjectDoesNotExist:
            category_name = None

        context['category_name'] = category_name

        # --

        brand_name = self.request.GET.get('brand')
        context['brand_name'] = brand_name

        price_sort_type = self.request.GET.get('price')
        context['price_sort_type'] = price_sort_type

        # --

        product_brands = Product.objects.values_list('brand', flat=True).distinct()
        # BRAND NAMES
        if category_name is None:
            brand_names = product_brands
        else:
            brand_names = product_brands.filter(category__id=category_id)

        context['brand_names'] = brand_names
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        categories = Category.objects.all()

        context['categories'] = categories

        return context


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


# Categories
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.objects.all()

        search = self.request.GET.get('search')

        if search is not None:
            categories = categories.filter(name__icontains=search)

        return categories


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
    template_name = 'update_category.html'
    model = Category
    context_object_name = 'categories1'
    fields = '__all__'
    success_url = reverse_lazy('categories')


# AUTHENTICATION
class Logout(LogoutView):
    next_page = 'products'


def signup_view(request):

    if request.method == 'POST':
        form = SignUpForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.image = form.cleaned_data.get('image')
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'registration/sign_up.html', {'form': form})


# PROFILE

class UserProfileDetailsView(DetailView):
    template_name = 'user_profile_view.html'
    model = Profile
    context_object_name = 'profile'


class UserProfileDeleteView(DeleteView):
    model = User
    template_name = 'profile_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('products')


def profile_update_view(request, pk):

    if request.method == 'POST':
        user_profile_form = UserProfileUpdateForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(data=request.POST, instance=request.user)

        if user_form.is_valid() and user_profile_form.is_valid():
            uform = user_form.save()
            upform = user_profile_form.save(commit=False)

            upform.user = uform
            upform.save()

            return redirect('profile_view', request.user.profile.id)
    else:
        user_profile_form = UserProfileUpdateForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)

        context = {
            'user_form': user_form,
            'user_profile_form': user_profile_form
        }

        return render(request, 'user_profile_update_view.html', context)


# Shopping Cart

class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'order_summary.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, 'You dont have an order')
            return render(self.request, 'order_summary.html', {})


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
        )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'The item quantity was updated')
            return redirect('product_details', pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request, 'The item was added to the cart')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'The item was added to the cart')

    return redirect('product_details', pk=pk)


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            order.items.remove(order_item)
            order_item.delete()

            messages.info(request, 'The item was removed from your cart')
            return redirect('order_summary')

        else:
            messages.info(request, 'You dont have that item in your cart')
            return redirect('product_details', pk=pk)

    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product_details', pk=pk)


@login_required
def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]

    order_item = OrderItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False,
        )[0]

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()

        messages.info(request, 'This item quantity was updated.')
    else:
        order.items.remove(order_item)
        order_item.delete()

        messages.info(request, 'The item was removed from your cart')

    return redirect('order_summary')


@login_required
def add_single_item_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]

    order_item.quantity += 1
    order_item.save()
    messages.info(request, 'The item quantity was updated')
    return redirect('order_summary')


class CheckoutView(View):

    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.info(self.request, 'Something went wrong! (CHECKOUT)')
            return redirect('products')

        form = CheckoutForm()
        # check if user has billing address
        billing_address = BillingAddress.objects.get(user=self.request.user)

        context = {
            'form': form,
            'order': order,
            'billing_address': billing_address,
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)

        # check if user has billing address
        # billing_address = BillingAddress.objects.get(user=self.request.user)

        if order_qs.exists():
            order = order_qs[0]

            """
                if billing_address:
                order.billing_address = billing_address
                order.save()
                return redirect('confirm_order')
            """

            if form.is_valid():

                street_address = form.cleaned_data.get('street_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                zip = form.cleaned_data.get('zip')
                country = form.cleaned_data.get('country')
                payment_options = form.cleaned_data.get('payment_options')

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    appartment_address=appartment_address,
                    zip=zip,
                    country=country,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                messages.info(self.request, 'Your checkout was successful!')
                return redirect('payment')

        else:
            messages.info(self.request, 'You dont have that an active order')
            return redirect('order_summary')

        messages.warning(self.request, 'Failed checkout')
        return redirect('checkout')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order,
        }

        return render(self.request, 'payment.html', context)


class FinishOrder(View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.info(self.request, 'Order did not go through')
            return redirect('products')

        for order_item in order.items.all():
            product_item = Product.objects.get(id=order_item.item.id)
            product_item.in_stock -= order_item.quantity
            product_item.save()

            order_item.ordered = True
            order_item.save()

            order.ordered = True
            order.save()

            messages.info(self.request, 'Order was succesful!')

            return redirect('products')
