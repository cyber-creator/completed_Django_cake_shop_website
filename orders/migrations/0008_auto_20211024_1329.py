# Generated by Django 3.2.8 on 2021-10-24 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_review_rating'),
        ('orders', '0007_alter_order_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderunit',
            name='cake',
        ),
        migrations.AddField(
            model_name='orderunit',
            name='cake',
            field=models.ManyToManyField(related_name='order_cake', to='catalog.Cake', verbose_name='order cakes'),
        ),
    ]
