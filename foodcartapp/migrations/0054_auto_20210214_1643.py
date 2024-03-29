# Generated by Django 3.0.7 on 2021-02-14 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0053_auto_20210214_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_method',
            field=models.CharField(blank=True, choices=[('CASH', 'Наличностью'), ('CARD', 'Электронно')], default='', max_length=4, verbose_name='способ оплаты'),
            preserve_default=False,
        ),
    ]
