# Generated by Django 2.1.5 on 2021-04-14 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0049_auto_20210414_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
