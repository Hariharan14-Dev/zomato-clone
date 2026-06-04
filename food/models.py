from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=100)
    address = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    delivery_time = models.IntegerField(default=30)  # minutes
    min_order = models.DecimalField(max_digits=8, decimal_places=2, default=100)
    image_url = models.URLField(blank=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_veg = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class DeliveryPerson(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    vehicle = models.CharField(max_length=50, default='Bike')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    is_available = models.BooleanField(default=True)
    profile_image = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('placed', 'Order Placed'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('picked', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('wallet', 'Wallet'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    estimated_delivery = models.IntegerField(default=30)  # minutes
    created_at = models.DateTimeField(auto_now_add=True)
    special_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity}x {self.food_item.name}"
