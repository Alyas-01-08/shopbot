# Generated by Django 4.1.2 on 2022-10-23 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingCart', '0002_alter_order_payment_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_system',
            field=models.CharField(blank=True, choices=[('visa/mastercard', 'Всемирная оплата'), ('rus', 'Оплата с России'), ('ton', 'Криптовалюта Ton'), ('binans', 'Binans')], max_length=50, null=True, verbose_name='Платежная система'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('creting', 'Ожидает оплаты'), ('new', 'Ожидает оплаты'), ('waiting', 'Ожидает оплаты'), ('paid', 'Оплачен'), ('canceled', 'Отменен')], default='creting', max_length=50, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(default=0, verbose_name='Общая сумма заказа'),
        ),
        migrations.AlterField(
            model_name='selectedproductbasket',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_products', to='shoppingCart.basket'),
        ),
        migrations.AlterField(
            model_name='selectedproductorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_products', to='shoppingCart.order'),
        ),
    ]
