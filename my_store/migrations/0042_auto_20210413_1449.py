# Generated by Django 2.1.5 on 2021-04-13 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0041_auto_20210413_1441'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='s_appartment_address',
            new_name='appartment_address',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='s_country',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='s_street_address',
            new_name='street_address',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='s_zip',
            new_name='zip',
        ),
    ]
