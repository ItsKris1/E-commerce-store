# Generated by Django 3.1.7 on 2021-04-01 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0012_profile_preferred_communication'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]