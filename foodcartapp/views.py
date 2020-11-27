import json


from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.templatetags.static import static


from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Product, Order, OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    order_data = request.data


    if 'products' not in order_data or not isinstance(order_data['products'], list) :
        return Response(
            data={'error': 'product key not presented or not list'},
            status=400
        )

    if 'firstname' not in order_data:
        return Response(
            data={'error': 'firstname not presented'},
            status=400
        )

    if not isinstance(order_data['firstname'], str):
        return Response(
            data={'error': 'The key \'firstname\' is not specified or not str'},
            status=400
        )
    for field, value in order_data.items():
        if not value:
            return Response(
                    data={'error': f'{field}  can not be null'},
                    status=400
                )

    if len(order_data['phonenumber']) < 1:
        return Response(
            data={'error': f'phonenumber  can not be empty'},
            status=400
        )

    avaliable_products = list(Product.objects.all().values_list('id', flat=True))

    for order_data in order_data['products']:
        if order_data['product'] not in avaliable_products:
            return Response(
                data={'error': f'unknown id for product'},
                status=400
            )

    order = Order.objects.create(
        firstname=order_data['firstname'],
        lastname=order_data['lastname'],
        address=order_data['address'],
        phonenumber=order_data['phonenumber']
    )

    for order_item in order_data['products']:
        OrderItem.objects.create(
            order=order,
            item_id=order_item['product'],
            count=order_item['quantity']
        )
    return JsonResponse({})
