from django.urls import path

from .views import IndexTemplateView, ProductListView, BasketTemplateView, OrderTemplateView, update_item, process_order

app_name = 'app_main'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('basket/', BasketTemplateView.as_view(), name='basket'),
    path('order/', OrderTemplateView.as_view(), name='order'),


    path('update_item/', update_item, name='update_item'),
    path('process_order/', process_order, name='process_order'),
]
