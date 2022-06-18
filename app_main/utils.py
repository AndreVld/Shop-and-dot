import json

from app_users.models import AdvUser
from .models import Product, Order, OrderItems


def cookie_basket(request):
    try:
        basket = json.loads(request.COOKIES['basket'])
    except:
        basket = {}

    items = []
    order = {'get_basket_items': 0, 'get_basket_total': 0, 'shipping': False}

    for product_id, quantity in basket.items():
        try:
            product = Product.objects.get(id=product_id)
            total = product.price * quantity['quantity']

            order['get_basket_total'] += total
            order['get_basket_items'] += quantity['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product,
                    'price': product.price,
                    'image_url': product.image_url,
                },
                'quantity': quantity['quantity'],
                'get_total': total,
            }
            items.append(item)

            if product.digital is False:
                order['shipping'] = True
        except:
            pass

    return {'items': items, 'order': order}


def basket_data(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitems_set.all()
        basket_items = order.get_basket_items
        basket_total = order.get_basket_total
    else:
        cookie_data = cookie_basket(request)
        items = cookie_data['items']
        order = cookie_data['order']
        basket_items = order['get_basket_items']
        basket_total = order['get_basket_total']

    return {'items': items, 'order': order, 'basket_items': basket_items, 'basket_total': basket_total, }


def guest_order(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_basket(request)
    items = cookie_data['items']

    customer, created = AdvUser.objects.get_or_create(email=email)
    customer.username = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        OrderItems.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order
