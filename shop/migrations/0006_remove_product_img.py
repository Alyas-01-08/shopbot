# Generated by Django 4.1.3 on 2022-11-01 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_prodictimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='img',
        ),
    ]
