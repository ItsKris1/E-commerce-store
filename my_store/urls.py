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

    path('bought_product/<int:pk>', views.ProductBuyView.as_view(), name='buy_product'),
    path('confirm_order/<int:pk>', views.ProductConfirmBuyView.as_view(), name='confirm_buy_product'),

    path('categories_list', views.CategoryListView.as_view(), name='categories'),
    path('create_category', views.CreateCategoryView.as_view(), name='create_category'),
    path('delete_category/<int:pk>', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('edit_category/<int:pk>', views.CategoryUpdateView.as_view(), name='edit_category'),


    path('accounts/log_out', views.LogoutView.as_view(), name='log_out'),
    path('accounts/login', views.LoginView.as_view(
        template_name="registration/login.html", authentication_form=UserLoginForm),
         name='login'),
    path('accounts/sign_up', views.signup_view, name='sign_up')
]

