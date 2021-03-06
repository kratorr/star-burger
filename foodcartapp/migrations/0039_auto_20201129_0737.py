# Generated by Django 3.0.7 on 2020-11-29 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20201125_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='count',
            new_name='quantity',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodcartapp.Product'),
        ),
    ]
