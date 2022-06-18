from django.contrib import admin

# Register your models here.
from app_main import models

admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderItems)
admin.site.register(models.ShippingAddress)
