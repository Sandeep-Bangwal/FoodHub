# Generated by Django 4.1.3 on 2023-09-12 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0012_alter_orders_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_address_details',
            name='order_add_id',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='cart',
        ),
        migrations.DeleteModel(
            name='order_address',
        ),
        migrations.DeleteModel(
            name='order_address_details',
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
    ]