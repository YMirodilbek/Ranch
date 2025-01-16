# Generated by Django 5.1.3 on 2024-11-25 05:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak.", regex='^\\+998\\d{9}$')]),
        ),
    ]
