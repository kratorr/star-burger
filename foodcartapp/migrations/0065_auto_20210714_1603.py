# Generated by Django 3.0.7 on 2021-07-14 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0064_auto_20210328_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
