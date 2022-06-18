from django.http import JsonResponse
from django.views.generic import ListView, TemplateView
from app_main.models import Product, Order, OrderItems, ShippingAddress
import datetime
import json

from app_main.utils import guest_order, basket_data


class IndexTemplateView(TemplateView):
    template_name = 'app_main/index.html'
    extra_context = {'title_': 'SHOP and .'}


class ProductListView(ListView):
    template_name = 'app_main/catalog.html'
    model = Product
    extra_context = {'title_': 'Products'}


class BasketTemplateView(ListView):
    template_name = 'app_main/basket.html'
    extra_context = {'title_': 'Basket'}
    context_object_name = 'items'

    def get_queryset(self):
        data = basket_data(self.request)
        return data['items']


class OrderTemplateView(ListView):
    template_name = 'app_main/order.html'
    extra_context = {'title_': 'Order', 'order': None}
    context_object_name = 'items'

    def get_queryset(self):
        data = basket_data(self.request)
        self.extra_context['order'] = data['order']
        print(self.extra_context['order'])
        return data['items']


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=request.user, complete=False)

    order_item, created = OrderItems.objects.get_or_create(product=product, order=order)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    if order_item.quantity <= 0:
        order_item.delete()
    else:
        order_item.save()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_basket_total):
        order.complete = True
    order.save()

    if order.shipping is True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            index=data['shipping']['index'],
            phone=data['shipping']['phone'],
        )
    return JsonResponse('Order completed successfully!', safe=False)
