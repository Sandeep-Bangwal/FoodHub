# Generated by Django 4.1.3 on 2023-05-13 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_alter_coupon_min_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='discount',
            field=models.IntegerField(default=100),
        ),
    ]
