# Generated by Django 5.2.1 on 2025-05-26 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_product_sub_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Sub_Category',
        ),
    ]
