from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=60)
    quantity = models.IntegerField(blank=True, default='None')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
