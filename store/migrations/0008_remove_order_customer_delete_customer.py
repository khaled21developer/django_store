# Generated by Django 5.1.3 on 2024-12-21 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_customer_order_city_order_phone_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
