from django.urls import path

from .forms import UserLoginForm
from . import views

urlpatterns = [
    # PRODUCTS
    path('products_list', views.ProductsListView.as_view(), name='products'),
    path('create_product', views.CreateProductView.as_view(), name='create_product'),
    path('product_details/<int:pk>', views.ProductDetailsView.as_view(), name='product_details'),
    path('delete_product/<int:pk>', views.ProductDeleteView.as_view(), name='delete_product'),
    path('update_product/<int:pk>', views.ProductUpdateView.as_view(), name='update_product'),

    # CATEGORIES
    path('categories_list', views.CategoryListView.as_view(), name='categories'),
    path('create_category', views.CreateCategoryView.as_view(), name='create_category'),
    path('delete_category/<int:pk>', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('edit_category/<int:pk>', views.CategoryUpdateView.as_view(), name='edit_category'),

    # SHOPPING CART
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<int:pk>', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('add_single_item_to_cart/<int:pk>', views.add_single_item_to_cart, name='add_single_item_to_cart'),
    path('shopping_cart', views.ShoppingCart.as_view(), name='shopping_cart'),

    # -
    path('billing_shipping', views.BillingShippingView.as_view(), name='billing_shipping'),

    # path('finished_order', views.FinishOrder.as_view(), name='finished_order'),
    path('payment', views.PaymentView.as_view(), name='payment'),
    path('payment_data', views.payment_data, name='payment_data'),
    path('payment_succesful', views.PaymentSuccessful.as_view(), name='payment_succesful'),
    # path('payment_cancelled', views.payment_canceled, name='payment_cancelled'),


    # AUTHENTICATION
    path('accounts/log_out', views.LogoutView.as_view(), name='log_out'),
    path('accounts/login/', views.LoginView.as_view(template_name="registration/login.html",
                                                    authentication_form=UserLoginForm), name='login'),
    path('accounts/sign_up', views.signup_view, name='sign_up'),

    # PROFILE
    path('profile/<int:pk>', views.UserProfileDetailsView.as_view(), name='profile_view'),
    path('profile/edit/<int:pk>', views.profile_update_view, name='profile_update_view'),
    path('profile/delete_user/<int:pk>', views.UserProfileDeleteView.as_view(), name='profile_delete')
]

