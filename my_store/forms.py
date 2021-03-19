from django import forms
from .models import Product, Category


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name',
                  'quantity',
                  'price',
                  'description',
                  'category',
                  )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
