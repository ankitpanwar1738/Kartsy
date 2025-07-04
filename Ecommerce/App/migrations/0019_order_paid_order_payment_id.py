# Generated by Django 5.2.1 on 2025-06-03 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0018_alter_order_address2'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
