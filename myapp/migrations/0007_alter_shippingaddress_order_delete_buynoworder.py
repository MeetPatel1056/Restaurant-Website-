# Generated by Django 5.1.2 on 2024-10-20 06:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_buynoworder_orderitem_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.order'),
        ),
        migrations.DeleteModel(
            name='BuyNowOrder',
        ),
    ]
