# Generated by Django 2.1.5 on 2021-04-14 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_store', '0051_auto_20210414_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='-', max_length=60),
        ),
    ]
