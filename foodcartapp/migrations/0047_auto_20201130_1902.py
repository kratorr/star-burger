# Generated by Django 3.0.7 on 2020-11-30 19:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_auto_20201130_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время звонка менеджера'),
        ),
        migrations.AddField(
            model_name='order',
            name='create_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='время получения заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, verbose_name='комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Необработанный'), ('DONE', 'Завершенный'), ('IN_PROG', 'Выполняется'), ('CANCEL', 'Отменён')], default='NEW', max_length=15, verbose_name='статус'),
        ),
    ]
