from django import forms
from .models import Product, Category, Profile

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User



class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name',
                  'brand',
                  'in_stock',
                  'price',
                  'description',
                  'category',
                  'image',

                  )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


"""AUTHENTICATION"""


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'hi'}
        )
    )

    password = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'type': 'password'}
        )
    )


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

    #
    username = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'Username'}))
    #
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'id': 'Password'}))

    #
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'id': 'Retype password'}))

    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'First name', 'placeholder': 'optional'}))

    #
    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'Last name', 'placeholder': 'optional'}))

    #
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'Email'}))

    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control', 'id': 'Profile picture'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  'first_name', 'last_name', 'email', 'profile_picture')




""""""


"""USER & PROFILE"""


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=15,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'Username'}))

    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'First name'}))

    #
    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'Last name'}))

    #
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'Email'}))

    profile_picture = forms.FileInput(attrs={'class ': 'form-control-file'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')



""""""

"""BILLING & SHIPPING"""


class AddressForm(forms.Form):
    # SHIPPING
    shipping_address1 = forms.CharField(required=False)

    shipping_address2 = forms.CharField(required=False)

    shipping_zip = forms.CharField(required=False)

    shipping_country = forms.CharField(required=False)

    # BILLING

    billing_address1 = forms.CharField(required=False)

    billing_address2 = forms.CharField(required=False)

    billing_zip = forms.CharField(required=False)

    billing_country = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)

    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)

    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)


""""""
