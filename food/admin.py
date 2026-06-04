from django.contrib import admin
from .models import Restaurant, FoodItem, Order, OrderItem, DeliveryPerson

admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryPerson)
