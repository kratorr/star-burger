from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.serializers import CharField
from rest_framework.validators import ValidationError


from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, write_only=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'address', 'phonenumber', 'products']
