# Generated by Django 2.1.5 on 2021-04-13 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0047_address_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='order_id',
        ),
    ]
