# Generated by Django 3.2.8 on 2021-10-22 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_transport_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='transport_cost',
            new_name='shipping',
        ),
    ]