# Generated by Django 4.1.2 on 2022-10-19 10:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=20, verbose_name='Размер')),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
                'ordering': ['value'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(to='shop.size'),
        ),
    ]
