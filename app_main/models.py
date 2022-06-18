from django.db import models

# Create your models here.
from app_users.models import AdvUser


class Product(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='products_img')
    name = models.CharField(max_length=256, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except ValueError:
            url = '/media/placeholder.png'
        return url


class Order(models.Model):
    customer = models.ForeignKey(AdvUser, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_basket_items(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_basket_total(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        for item in self.orderitems_set.all():
            if item.product.digital is False:
                shipping = True
                break
        return shipping


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(AdvUser, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=128, null=True)
    city = models.CharField(max_length=128, null=True)
    index = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=128, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
