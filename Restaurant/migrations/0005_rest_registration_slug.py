# Generated by Django 4.1.3 on 2023-05-07 14:11

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0004_alter_rest_registration_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='rest_registration',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='rest_name', unique=True),
        ),
    ]
