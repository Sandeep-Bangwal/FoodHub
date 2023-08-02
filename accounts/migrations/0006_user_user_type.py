# Generated by Django 4.1.3 on 2023-04-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_user_is_active_remove_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('customer', 'Customer'), ('restaurant', 'restaurant')], default='', max_length=10),
            preserve_default=False,
        ),
    ]