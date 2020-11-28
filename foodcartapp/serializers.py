from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.serializers import CharField
from rest_framework.validators import ValidationError


from .models import  Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, write_only=True)

    def validate_products(self, value):
        if not len(value):
            raise ValidationError('Это поле не может быть пустым')
        return value

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'address', 'phonenumber', 'products']
