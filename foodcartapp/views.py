from itertools import product
from xml.dom import ValidationErr
import phonenumbers
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField

from rest_framework.serializers import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ListField


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


@api_view(['GET'])
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
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'amount']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ['address', 'firstname',
                  'lastname', 'phonenumber', 'products']


@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order_items = serializer.validated_data
    firstname = order_items['firstname']
    phone = phonenumbers.parse(order_items['phonenumber'], 'RU')
    order = Order.objects.create(
        firstname=firstname,
        lastname=order_items['lastname'],
        phonenumber=phone,
        address=order_items['address'],
    )
    order_products = order_items['products']
    for order_product in order_products:
        product = Product.objects.get(id=order_product['product'])
        OrderItem.objects.update_or_create(
            order=order,
            product=product,
            amount=order_product['quantity']
        )
    return Response({})
