# Generated by Django 4.1.2 on 2022-11-07 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_category_image'),
        ('shoppingCart', '0004_alter_order_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedproductbasket',
            name='size',
            field=models.CharField(default='40', max_length=10, verbose_name='Размер'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='selectedproductorder',
            name='size',
            field=models.CharField(default='40', max_length=10, verbose_name='Размер'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='selectedproductbasket',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_products_basket', to='shoppingCart.basket'),
        ),
        migrations.AlterField(
            model_name='selectedproductbasket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_product', to='shop.product'),
        ),
    ]
