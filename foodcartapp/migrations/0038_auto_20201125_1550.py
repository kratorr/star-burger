# Generated by Django 3.0.7 on 2020-11-25 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0037_auto_20201125_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='telephone_number',
            new_name='phonenumber',
        ),
    ]