# Generated by Django 5.2.1 on 2025-05-29 19:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_product_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='Brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.brand'),
        ),
    ]
