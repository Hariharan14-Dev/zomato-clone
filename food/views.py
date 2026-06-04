from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Restaurant, FoodItem, Order, OrderItem, DeliveryPerson
import json, random

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password')
    return render(request, 'food/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'food/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    restaurants = Restaurant.objects.filter(is_open=True)
    return render(request, 'food/home.html', {'restaurants': restaurants})

@login_required
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menu = restaurant.menu_items.all()
    starters = menu.filter(category='starter')
    mains = menu.filter(category='main')
    desserts = menu.filter(category='dessert')
    beverages = menu.filter(category='beverage')
    return render(request, 'food/restaurant.html', {
        'restaurant': restaurant,
        'starters': starters,
        'mains': mains,
        'desserts': desserts,
        'beverages': beverages,
    })

@login_required
def cart(request):
    return render(request, 'food/cart.html')

@login_required
def checkout(request):
    if request.method == 'POST':
        cart_data = request.POST.get('cart_data', '{}')
        payment_method = request.POST.get('payment_method', 'cod')
        delivery_address = request.POST.get('delivery_address', '')
        special_instructions = request.POST.get('special_instructions', '')
        
        try:
            cart_items = json.loads(cart_data)
        except:
            cart_items = {}

        if not cart_items:
            messages.error(request, 'Cart is empty!')
            return redirect('cart')

        first_item_id = list(cart_items.keys())[0]
        food_item = get_object_or_404(FoodItem, pk=first_item_id)
        restaurant = food_item.restaurant

        total = sum(
            float(FoodItem.objects.get(pk=item_id).price) * qty
            for item_id, qty in cart_items.items()
            if FoodItem.objects.filter(pk=item_id).exists()
        )
        total += 40  # delivery fee

        delivery_people = DeliveryPerson.objects.filter(is_available=True)
        delivery_person = delivery_people.order_by('?').first() if delivery_people.exists() else None

        order = Order.objects.create(
            user=request.user,
            restaurant=restaurant,
            delivery_person=delivery_person,
            payment_method=payment_method,
            total_amount=total,
            delivery_address=delivery_address,
            estimated_delivery=restaurant.delivery_time + random.randint(0, 15),
            special_instructions=special_instructions,
        )

        for item_id, qty in cart_items.items():
            try:
                food = FoodItem.objects.get(pk=item_id)
                OrderItem.objects.create(order=order, food_item=food, quantity=qty, price=food.price)
            except FoodItem.DoesNotExist:
                pass

        return redirect('order_success', pk=order.pk)
    return redirect('cart')

@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'food/order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'food/my_orders.html', {'orders': orders})
