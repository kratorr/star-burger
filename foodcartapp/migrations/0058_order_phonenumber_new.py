# Generated by Django 3.0.7 on 2021-03-27 12:58

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0057_auto_20210327_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phonenumber_new',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
    ]
