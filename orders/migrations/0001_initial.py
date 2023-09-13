# Generated by Django 4.1.3 on 2023-09-12 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Home', '0013_remove_order_address_details_order_add_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='order_address',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razorpay_order_id', models.CharField(max_length=100, unique=True)),
                ('total_amounts', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Order Recieved', 'Order Recieved'), ('Baking', 'Baking'), ('Baked', 'Baked'), ('Out for delivery', 'Out for delivery'), ('delivered ', 'delivered ')], default='Order Recieved', max_length=50)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_cart', to='Home.cart')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='order_address_details',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=50)),
                ('mob_no', models.CharField(max_length=12)),
                ('line', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipCode', models.IntegerField()),
                ('order_add_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='orders.order_address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]