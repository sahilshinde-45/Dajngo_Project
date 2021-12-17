# Generated by Django 3.2.7 on 2021-11-30 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('Eshopper', '0008_alter_orderitem_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_order',
            name='coupon_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.coupon'),
        ),
        migrations.AlterField(
            model_name='user_order',
            name='payment_gateway_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.payment_gateway'),
        ),
    ]
