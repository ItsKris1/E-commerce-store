from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=120)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)

    OWNER = 'Owner'
    ADMIN = 'Admin'
    USER = 'User'

    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (ADMIN, 'Admin'),
        (USER, 'User'),
    ]

    role = models.CharField(max_length=5,
                            choices=ROLE_CHOICES,
                            default=USER,
                            )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

