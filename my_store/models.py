from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=60)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name
