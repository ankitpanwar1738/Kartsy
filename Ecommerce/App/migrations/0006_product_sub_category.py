# Generated by Django 5.2.1 on 2025-05-26 18:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_alter_product_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Sub_Category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.sub_category'),
        ),
    ]
