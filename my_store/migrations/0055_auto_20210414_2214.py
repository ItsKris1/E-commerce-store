# Generated by Django 2.1.5 on 2021-04-14 19:14

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0054_auto_20210414_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
