# Generated by Django 3.0.7 on 2021-03-28 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0060_auto_20210328_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='phonenumber',
        ),
    ]
