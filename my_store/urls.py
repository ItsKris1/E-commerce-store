from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm
urlpatterns = [
    path('products_list', views.ProductsListView.as_view(), name='products'),
    path('create_product', views.CreateProductView.as_view(), name='create_product'),
    path('product_details/<int:pk>', views.ProductDetailsView.as_view(), name='product_details'),
    path('delete_product/<int:pk>', views.ProductDeleteView.as_view(), name='delete_product'),
    path('update_product/<int:pk>', views.ProductUpdateView.as_view(), name='update_product'),

    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<int:pk>', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('add_single_item_to_cart/<int:pk>', views.add_single_item_to_cart, name='add_single_item_to_cart'),

    path('order_summary', views.OrderSummary.as_view(), name='order_summary'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
    path('confirm_order', views.ConfirmOrder.as_view(), name='confirm_order'),
    path('finished_order', views.FinishOrder.as_view(), name='finished_order'),


    path('categories_list', views.CategoryListView.as_view(), name='categories'),
    path('create_category', views.CreateCategoryView.as_view(), name='create_category'),
    path('delete_category/<int:pk>', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('edit_category/<int:pk>', views.CategoryUpdateView.as_view(), name='edit_category'),


    path('accounts/log_out', views.LogoutView.as_view(), name='log_out'),
    path('accounts/login/', views.LoginView.as_view(
        template_name="registration/login.html", authentication_form=UserLoginForm),
         name='login'),
    path('accounts/sign_up', views.signup_view, name='sign_up'),

    path('profile/<int:pk>', views.UserProfileDetailsView.as_view(), name='profile_view'),
    path('profile/edit/<int:pk>', views.profile_update_view, name='profile_update_view'),
    path('profile/delete_user/<int:pk>', views.UserProfileDeleteView.as_view(), name='profile_delete')
]

