# Generated by Django 3.1.7 on 2021-04-03 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0028_auto_20210403_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]