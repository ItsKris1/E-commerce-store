# Generated by Django 3.1.7 on 2021-03-28 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
        ),
    ]
