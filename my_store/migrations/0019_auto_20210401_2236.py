# Generated by Django 3.1.7 on 2021-04-01 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0018_auto_20210401_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('OWNER', 'Owner'), ('ADMIN', 'Admin'), ('USER', 'User')], default='User', max_length=5),
        ),
    ]
