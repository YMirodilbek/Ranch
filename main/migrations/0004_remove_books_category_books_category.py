# Generated by Django 5.1.3 on 2024-11-25 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_category_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='category',
        ),
        migrations.AddField(
            model_name='books',
            name='category',
            field=models.ManyToManyField(to='main.category'),
        ),
    ]
