# Generated by Django 3.0.7 on 2020-11-25 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0036_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='last_name',
            new_name='lastname',
        ),
    ]