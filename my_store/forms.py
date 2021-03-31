from django import forms
from .models import Product, Category
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name',
                  'quantity',
                  'price',
                  'description',
                  'category',
                  'image',
                  )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
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


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
            'password2': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),

        }