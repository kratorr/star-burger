from django.db import models
from django.core.validators import MinValueValidator

from django.db.models import Sum, F
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField('контактный телефон', max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='категория', related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False, db_index=True)
    description = models.TextField('описание', max_length=200, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items',
                                   verbose_name="ресторан")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='menu_items',
                                verbose_name='продукт')
    availability = models.BooleanField('в продаже', default=True, db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]


class OrderQuerySet(models.QuerySet):

    def fetch_with_order_cost(self):
        return self.annotate(
            order_cost=Sum('order_items__amount')
        )


class Order(models.Model):
    STATUSES = [
        ('NEW', 'Необработанный'),
        ('DONE', 'Завершенный'),
        ('IN_PROG', 'Выполняется'),
        ('CANCEL', "Отменён")
    ]

    PAY_METHODS = [
        ('CASH', 'Наличностью'),
        ('CARD', 'Электронно')
    ]

    firstname = models.CharField(max_length=50, verbose_name='имя')
    lastname = models.CharField(max_length=50, verbose_name='фамилия')
    phonenumber = models.CharField(max_length=15, verbose_name='телефон')
    address = models.CharField(max_length=100, verbose_name='адрес доставки')
    status = models.CharField(max_length=15, choices=STATUSES, default='NEW', verbose_name='статус')
    comment = models.TextField(verbose_name='комментарий', blank=True)
    create_at = models.DateTimeField(default=timezone.now, verbose_name='время получения заказа')
    called_at = models.DateTimeField(verbose_name='время звонка менеджера', blank=True, null=True)
    delivered_at = models.DateTimeField(verbose_name='время доставки', blank=True, null=True)
    pay_method = models.CharField(max_length=4, choices=PAY_METHODS, verbose_name='способ оплаты', null=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, null=True, blank=False)

    objects = OrderQuerySet.as_manager()

    def __str__(self):
        return f"{self.lastname} - {self.address}"

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', validators=[
        MinValueValidator(1), MaxValueValidator(50)
        ]
    )
    amount = models.DecimalField(verbose_name='сумма', max_digits=8, decimal_places=2, null=False)

    def __str__(self):
        return f"Order: {self.order.id} - {self.product.name} - {self.quantity}"


    class Meta:
        verbose_name = 'пункт заказа'
        verbose_name_plural = 'пункты заказа'
