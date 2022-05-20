import phonenumbers
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework.decorators import api_view
from rest_framework import status
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


@api_view(['POST'])
def register_order(request):
    try:
        order_items = request.data
        name = order_items['firstname']
        if not isinstance(name, str):
            return Response({'error': 'name: Not a valid string'})
        phone = phonenumbers.parse(order_items['phonenumber'], 'RU')
        order = Order.objects.create(
            name=name,
            last_name=order_items['lastname'],
            phone=phone,
            address=order_items['address'],
        )
        order_products = order_items['products']
        if not order_products:
            return Response({'error': 'products: Этот список не может быть пустым.'})
        for order_product in order_products:
            product = Product.objects.get(id=order_product['product'])
            OrderItem.objects.update_or_create(
                order=order,
                product=product,
                amount=order_product['quantity']
            )
        return Response({})
    except Product.DoesNotExist as error:
        return Response({'error': f'{error}'})
    except phonenumbers.phonenumberutil.NumberParseException as error:
        return Response({'error': f'{error}'})
    except IntegrityError as error:
        return Response({'error': f'{error}'})
    except TypeError as error:
        return Response({'error': f'{error}'})
    except KeyError as error:
        return Response({'error': f'Not key {error}'})
