from django import forms
from .models import Product, Category, Profile, ShippingAddress

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from django_countries.fields import CountryField


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
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
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
    username = forms.CharField(max_length=15,widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'Username'}))
    #
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'id': 'Password'}))

    #
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'id': 'Retype password'}))

    #
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'First name'}))

    #
    last_name = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'Last name'}))

    #
    email = forms.EmailField(required=False, widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'Email'}))

    #
    location = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'Location'}))

    #
    image = forms.ImageField(required=False, widget=forms.FileInput(
            attrs={'class': 'form-control', 'id': 'Profile picture'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'location', 'password1', 'password2',
                  'image')


""""""


"""USER & PROFILE"""


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=15,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'Username'}))

    class Meta:
        model = User
        fields = ('username',)


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (

            'first_name',
            'last_name',
            'location',
            'email',
            'profile_picture'
        )

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class ': 'form-control-file'}),
        }


""""""

"""BILLING & SHIPPING"""


class BillingForm(forms.Form):

    street_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Main st 1234'}))

    appartment_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Apartment, suite number'}))

    zip = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Postal code'}))

    country = CountryField(blank_label='Select country').formfield(widget=forms.Select(
        attrs={'class': 'form-control'}))


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('street_address', 'appartment_address', 'zip', 'country')

        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'appartment_address':  forms.TextInput(attrs={'class': 'form-control'}),
            'zip': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }


""""""
