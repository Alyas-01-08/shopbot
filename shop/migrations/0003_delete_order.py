# Generated by Django 4.1.2 on 2022-10-17 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_rename_сategory_product_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
