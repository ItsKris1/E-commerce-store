from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django_countries.fields import CountryField
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=120)
    in_stock = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item.name} - {self.quantity}x'

    def get_total_price(self):
        return self.item.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)

    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0

        for order_item in self.items.all():
            total = total + order_item.get_total_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    appartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    country = CountryField(multiple=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

