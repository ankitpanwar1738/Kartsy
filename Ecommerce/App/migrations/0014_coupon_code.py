# Generated by Django 5.2.1 on 2025-05-31 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_product_packing_cost_product_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon_Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField()),
            ],
        ),
    ]
