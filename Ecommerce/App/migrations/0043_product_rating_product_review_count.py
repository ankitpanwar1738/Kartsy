# Generated by Django 5.2.1 on 2025-06-21 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0042_order_cancelled_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
    ]
