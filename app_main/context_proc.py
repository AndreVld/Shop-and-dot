from .utils import basket_data


def basket(request):
    data = basket_data(request)

    return {'basket_items': data['basket_items'], 'basket_total': data['basket_total'], }
