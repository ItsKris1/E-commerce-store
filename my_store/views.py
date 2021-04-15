
from .models import Product, Category, Profile, OrderItem, Order, Address
from .forms import ProductCreateForm, CategoryCreateForm, SignUpForm, UserProfileUpdateForm, UserUpdateForm, AddressForm, ProfileSignUpForm
import requests
import json
from django.http import JsonResponse

from paypalrestsdk import Payment
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView, View, FormView
from django.urls import reverse_lazy
from django.conf import settings

from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404


"""PRODUCTS 1"""


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'

    """QUERYSETS"""
    def get_queryset(self):
        products = Product.objects.all()

        # SORT BY PRICE
        price = self.request.GET.get('price', None)
        if price == 'desc':
            products = products.order_by('-price')

        if price == 'asc':
            products = products.order_by('price')

        # SORT BY BRAND
        brand = self.request.GET.get('brand', None)
        if brand is not None:
            products = products.filter(brand__iexact=brand)
        #

        # SORT BY SEARCH
        search = self.request.GET.get('search', None)
        if search is not None:
            products = products.filter(name__icontains=search)
        #

        # SORT BY CATEGORY
        category_id = self.request.GET.get('category', None)
        if category_id is not None:
            products = products.filter(category__id=int(category_id))
        #

        return products

    """CONTEXT"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        # CATEGORIES
        categories = Category.objects.all()
        context['categories'] = categories

        # CATEGORY NAME
        category_id = self.request.GET.get('category', None)
        try:
            category_name = Category.objects.get(pk=category_id)
        except ObjectDoesNotExist:
            category_name = None

        context['category_name'] = category_name

        # BRAND NAME FROM URL
        brand_name = self.request.GET.get('brand')
        context['brand_name'] = brand_name

        # PRICE SORT TYPE
        price_sort_type = self.request.GET.get('price')
        context['price_sort_type'] = price_sort_type
        #

        # ALL BRAND NAMES ON - ALL PRODUCTS or CATEGORIES
        product_brands = Product.objects.values_list('brand', flat=True).distinct()

        if category_name is None:
            brand_names = product_brands
        else:
            brand_names = product_brands.filter(category__id=category_id)

        context['brand_names'] = brand_names

        return context


""""""
#
"""PRODUCTS 2"""


class CreateProductView(CreateView, PermissionRequiredMixin):
    permission_required = ['my_store.add_product']
    template_name = 'products/create_product.html'
    form_class = ProductCreateForm
    model = Product
    success_url = reverse_lazy('products')


class ProductDetailsView(DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        categories = Category.objects.all()

        context['categories'] = categories

        return context


class ProductDeleteView(DeleteView, PermissionRequiredMixin):
    permission_required = ['my_store.delete_product']

    template_name = 'products/product_confirm_delete.html'
    model = Product
    success_url = reverse_lazy('products')
    context_object_name = 'products'


class ProductUpdateView(UpdateView, PermissionRequiredMixin):
    permission_required = ['my_store.change_product']

    def get_success_url(self):
        return reverse_lazy('product_details', args=(self.object.id,))

    template_name = 'products/update_product.html'
    model = Product
    form_class = ProductCreateForm
    context_object_name = 'products'


""""""
#
"""CATEGORIES"""


class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.objects.all()

        search = self.request.GET.get('search')

        if search is not None:
            categories = categories.filter(name__icontains=search)

        return categories


class CreateCategoryView(CreateView, PermissionRequiredMixin):
    permission_required = ['my_store.create_category']

    template_name = 'category/create_category.html'
    form_class = CategoryCreateForm
    model = Category
    # fields = '__all__'
    success_url = reverse_lazy('categories')


class CategoryDeleteView(DeleteView, PermissionRequiredMixin):
    permission_required = ['my_store.delete_category']

    template_name = 'category/category_confirm_delete.html'
    model = Category
    success_url = reverse_lazy('categories')
    context_object_name = 'categories1'


class CategoryUpdateView(UpdateView):
    template_name = 'category/update_category.html'
    model = Category
    context_object_name = 'categories1'
    fields = '__all__'
    success_url = reverse_lazy('categories')


""""""
#
"""AUTHENTICATION"""


class Logout(LogoutView):
    next_page = 'products'


def signup_view(request):

    if request.method == 'POST':
        user_form = SignUpForm(data=request.POST)
        profile_form = ProfileSignUpForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()

            user.profile.first_name = user_form.cleaned_data.get('first_name')
            user.profile.last_name = user_form.cleaned_data.get('last_name')
            user.profile.email = user_form.cleaned_data.get('email')
            user.profile.country = profile_form.cleaned_data.get('country')
            user.profile.profile_picture = profile_form.cleaned_data.get('profile_picture')
            user.save()
            user.profile.save()

            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            authenticate(username=username, password=raw_password)
            messages.info(request, 'User registered succesfully!')
            # login(request, user)
            return redirect('login')
    else:
        user_form = SignUpForm()
        profile_form = ProfileSignUpForm()

    return render(request, 'registration/sign_up.html', {'user_form': user_form, 'profile_form': profile_form})


""""""
#
"""USER & PROFILE"""


class UserProfileDetailsView(DetailView):
    template_name = 'profile/user_profile_view.html'
    model = Profile
    context_object_name = 'profile'


class UserProfileDeleteView(DeleteView):
    model = User
    template_name = 'profile/profile_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('products')


def profile_update_view(request, pk):

    if request.method == 'POST':
        user_profile_form = UserProfileUpdateForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(data=request.POST, instance=request.user)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()

            user.profile.first_name = user_form.cleaned_data.get('first_name')
            user.profile.last_name = user_form.cleaned_data.get('last_name')
            user.profile.email = user_form.cleaned_data.get('email')
            user.profile.country = user_profile_form.cleaned_data.get('country')
            user.profile.profile_picture = user_profile_form.cleaned_data.get('profile_picture')
            user.save()
            user.profile.save()

            return redirect('profile_view', request.user.profile.id)
    else:
        user_profile_form = UserProfileUpdateForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)

        context = {
            'user_form': user_form,
            'user_profile_form': user_profile_form
        }

        return render(request, 'profile/user_profile_update_view.html', context)


""""""
#
"""PAYMENT"""


class PaymentView(View):

    def get(self, *args, **kwargs):

        order = Order.objects.get(user=self.request.user, ordered=False)
        shipping_address = order.shipping_address
        billing_address = order.billing_address
        context = {
            'order': order,
            'shipping_address': shipping_address,
            'billing_address': billing_address,

        }
        return render(self.request, 'payment.html', context)


class PaymentSuccessful(View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            for order_item in order.items.all():
                product_item = Product.objects.get(id=order_item.item.id)
                product_item.in_stock -= order_item.quantity
                product_item.save()

                order_item.ordered = True
                order_item.save()

                order.ordered = True
                order.save()

                messages.info(self.request, 'Order was succesful!')
                return render(self.request, 'payment_succesful.html', {})

        except ObjectDoesNotExist:
            messages.info(self.request, 'You dont have an existing order.')
            return redirect('products')


# For getting data through PayPal
def payment_data(request):

    body = json.loads(request.body)
    print('body -->', body)
    return redirect('products')


""""""
#
"""BILLING & SHIPPING"""


class BillingShippingView(View):

    def get(self, *args, **kwargs):
        form = AddressForm()

        context = {
            'form': form,
        }

        address_qs = Address.objects.filter(
            user=self.request.user,
            address_type='S',
            default_address=True)

        if address_qs.exists():
            context.update(
                {'default_shipping_address': address_qs[0]}
            )

        return render(self.request, 'billing_shipping.html', context)

    #
    def post(self, *args, **kwargs):
        form = AddressForm(self.request.POST or None)
        try:
            # Just in case checking if user has an active order
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                # Gets user input on what he wants to do
                same_billing_address = form.cleaned_data.get('same_billing_address')
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                set_default_shipping = form.cleaned_data.get('set_default_shipping')

                # If user wants to use default shipping address
                if use_default_shipping:
                    address_qs = Address.objects.filter(user=self.request.user, default_address=True, address_type='S')
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                    else:
                        messages.info(self.request, 'No default shipping address available!')
                        return redirect('billing_shipping')

                # Else..
                else:
                    shipping_address1 = form.cleaned_data.get('shipping_address1')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_zip = form.cleaned_data.get('shipping_zip')
                    shipping_country = form.cleaned_data.get('shipping_country')

                    shipping_address = Address(
                        user=self.request.user,
                        street_address=shipping_address1,
                        appartment_address=shipping_address2,
                        zip=shipping_zip,
                        country=shipping_country,
                        address_type='S'
                    )

                    # If user wants to make added shipping address as a Default
                    if set_default_shipping:
                        address_qs = Address.objects.filter(user=self.request.user, default_address=True,
                                                            address_type='S')
                        if address_qs.exists():
                            old_default_address = address_qs[0]
                            old_default_address.default_address = False
                            old_default_address.save()
                        else:

                            shipping_address.default_address = True

                # After the conditions on filling the shipping address, we check whether
                # billing address and shipping address are the same
                if same_billing_address:
                    billing_address = Address(
                        user=self.request.user,
                        street_address=shipping_address.street_address,
                        appartment_address=shipping_address.appartment_address,
                        zip=shipping_address.zip,
                        country=shipping_address.country,

                        address_type='B'
                    )
                # If billing address and shipping address are not the same...
                else:

                    # Getting user input
                    use_default_billing = form.cleaned_data.get('use_default_billing')

                    # If user has chosen Default billing address
                    if use_default_billing:
                        address_qs = Address.objects.filter(user=self.request.user, default_address=True,
                                                            address_type='B')
                        if address_qs.exists():
                            billing_address = address_qs[0]

                        else:
                            messages.info(self.request, 'No default shipping address available!')
                            return redirect('billing_shipping')
                    # Else... we just take user address
                    else:

                        # HANDELING BILLING FORM
                        billing_address1 = form.cleaned_data.get('billing_address1')
                        billing_address2 = form.cleaned_data.get('billing_address2')
                        billing_zip = form.cleaned_data.get('billing_zip')
                        billing_country = form.cleaned_data.get('billing_country')

                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            appartment_address=billing_address2,
                            zip=billing_zip,

                            address_type='B'
                        )
                        # If user wants to make added address Default address
                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            address_qs = Address.objects.filter(user=self.request.user, default_address=True,
                                                                address_type='B')
                            if address_qs.exists():
                                old_default_address = address_qs[0]
                                old_default_address.default_address = False
                                old_default_address.save()
                            else:

                                billing_address.default_address = True

                # Now we are saving all the addresses after going through conditions
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()

                messages.info(self.request, 'Addresses were entered succesfully!')
                return redirect('payment')

        # If for some reason user does not have an active order
        except ObjectDoesNotExist:
            messages.error(self.request, 'You dont have an active order!')
            return redirect('products')


#
"""SHOPPING CART"""


class ShoppingCart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'shopping_cart.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, 'Your shopping cart is empty.')
            return redirect('products')


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
            return redirect('shopping_cart')

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

    return redirect('shopping_cart')


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
    return redirect('shopping_cart')


""""""


