
# 🍕 Zomato Clone — Django Full Stack

A complete food delivery app clone built with Django.

## Features
- ✅ User Registration & Login
- ✅ Browse Restaurants (6 pre-loaded)
- ✅ View Full Menu by Category (Starter, Main, Dessert, Beverage)
- ✅ Add/Remove items from Cart
- ✅ Checkout with Address & Payment Method
- ✅ Delivery Person assignment (name, phone, rating, vehicle)
- ✅ Live Order Tracking UI
- ✅ Order History page
- ✅ Django Admin Panel

## Quick Setup

```bash
# 1. Install dependencies
pip install django pillow

# 2. Apply migrations
python manage.py migrate

# 3. Load sample data
python manage.py seed_data

# 4. Run the server
python manage.py runserver
```

## Login Credentials
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| User | testuser | test123 |

## URLs
- Home: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/login/
- Admin: http://127.0.0.1:8000/admin/
- Cart: http://127.0.0.1:8000/cart/
- My Orders: http://127.0.0.1:8000/my-orders/

## Project Structure
```
zomato_clone/
├── manage.py
├── zomato/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── food/
│   ├── models.py         # Restaurant, FoodItem, Order, DeliveryPerson
│   ├── views.py          # All page views
│   ├── admin.py          # Admin panel config
│   └── management/
│       └── commands/
│           └── seed_data.py   # Sample data loader
└── templates/
    └── food/
        ├── base.html
        ├── login.html
        ├── register.html
        ├── home.html          # Restaurant listing
        ├── restaurant.html    # Menu page
        ├── cart.html          # Cart & checkout
        ├── order_success.html # Order confirmation
        ├── my_orders.html     # Order history
        └── partials/
            └── food_item.html
```

## Models
- **Restaurant** — name, cuisine, address, rating, delivery_time, min_order
- **FoodItem** — name, description, price, category, is_veg (linked to Restaurant)
- **DeliveryPerson** — name, phone, vehicle, rating
- **Order** — user, restaurant, delivery_person, status, payment_method, total, address
- **OrderItem** — order, food_item, quantity, price
