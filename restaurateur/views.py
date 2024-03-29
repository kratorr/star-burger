from collections import defaultdict


from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views


from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem

from .utils import fetch_coordinates

from geopy import distance as d


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_items.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })



@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    restaurants_items = RestaurantMenuItem.objects.filter(availability=True).select_related('restaurant', 'product')
    restraunts_menu = defaultdict(set)
    for item in restaurants_items:
        restraunts_menu[(item.restaurant.id, item.restaurant.name, item.restaurant.address)].add(item.product_id)

    orders = Order.objects.fetch_with_order_cost().prefetch_related('order_items__product')

    for order in orders:
        order.restaurants = []
        order_products = set(item.product_id for item in order.order_items.all())

        for item in restraunts_menu.items():
            restaurant, restaurant_products = item
            _, restaurant_name, restaurant_address = restaurant
            if restaurant_products.issubset(order_products):

                restaurant_cache_key = restaurant_address.replace(' ', '')
                restaurant_coordinates = cache.get(restaurant_cache_key)
                if not restaurant_coordinates:
                    restaurant_coordinates = fetch_coordinates(settings.GEOCODER_API_KEY, restaurant_address)
                    cache.set(restaurant_cache_key, restaurant_coordinates)

                customer_cache_key = order.address.replace(' ', '')
                customer_coordinates = cache.get(customer_cache_key)
                if not customer_coordinates:
                    customer_coordinates = fetch_coordinates(settings.GEOCODER_API_KEY, order.address)
                    cache.set(customer_cache_key, customer_coordinates)

                distance = d.distance(restaurant_coordinates, customer_coordinates).km
                order.restaurants.append((distance, restaurant_name))

        order.restaurants = sorted(order.restaurants, key=lambda restaurant: restaurant[0])
    return render(request, template_name='order_items.html', context={
        'orders': orders
    })
