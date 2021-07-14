# Generated by Django 3.0.7 on 2021-03-27 07:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0056_auto_20210214_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='время звонка менеджера'),
        ),
        migrations.AlterField(
            model_name='order',
            name='create_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='время получения заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='время доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pay_method',
            field=models.CharField(blank=True, choices=[('CASH', 'Наличностью'), ('CARD', 'Электронно')], db_index=True, max_length=4, verbose_name='способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Необработанный'), ('DONE', 'Завершенный'), ('IN_PROG', 'Выполняется'), ('CANCEL', 'Отменён')], db_index=True, default='NEW', max_length=15, verbose_name='статус'),
        ),
    ]