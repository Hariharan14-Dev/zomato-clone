from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from food.models import Restaurant, FoodItem, DeliveryPerson

class Command(BaseCommand):
    help = 'Seed sample data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@zomato.com', 'admin123')
            self.stdout.write('Created admin: admin / admin123')

        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user('testuser', 'test@test.com', 'test123')
            self.stdout.write('Created testuser: testuser / test123')

        for d in [
            {'name': 'Ravi Kumar', 'phone': '9876543210', 'vehicle': 'Bike', 'rating': 4.8},
            {'name': 'Suresh Babu', 'phone': '9876543211', 'vehicle': 'Scooter', 'rating': 4.6},
            {'name': 'Anbu Selvan', 'phone': '9876543212', 'vehicle': 'Bike', 'rating': 4.9},
            {'name': 'Karthik Raja', 'phone': '9876543213', 'vehicle': 'Bike', 'rating': 4.7},
        ]:
            DeliveryPerson.objects.get_or_create(phone=d['phone'], defaults=d)

        restaurants = [
            {'meta': {'name': 'Spice Garden', 'cuisine': 'North Indian', 'address': '12 MG Road, Tiruppur', 'rating': 4.5, 'delivery_time': 30, 'min_order': 150},
             'menu': [('Paneer Tikka','Marinated paneer grilled in tandoor',180,'starter',True),('Chicken Tikka','Boneless chicken in spiced marinade',220,'starter',False),('Butter Chicken','Tender chicken in creamy tomato gravy',280,'main',False),('Dal Makhani','Slow-cooked black lentils with butter',200,'main',True),('Paneer Butter Masala','Paneer in tomato-cashew gravy',240,'main',True),('Garlic Naan','Soft bread baked in tandoor',50,'main',True),('Gulab Jamun','Milk dumplings in sugar syrup',80,'dessert',True),('Mango Lassi','Yogurt drink with fresh mangoes',80,'beverage',True)]},
            {'meta': {'name': 'Chennai Express', 'cuisine': 'South Indian', 'address': '45 Avinashi Road, Tiruppur', 'rating': 4.3, 'delivery_time': 25, 'min_order': 100},
             'menu': [('Idli (3pcs)','Steamed rice cakes with sambar',60,'starter',True),('Vada (2pcs)','Crispy lentil doughnuts',70,'starter',True),('Masala Dosa','Crispy crepe with potato masala',90,'main',True),('Ghee Pongal','Rice and lentil porridge with ghee',80,'main',True),('Chettinad Chicken Curry','Spicy Chettinad chicken',200,'main',False),('Semiya Payasam','Vermicelli pudding in milk',70,'dessert',True),('Filter Coffee','Traditional South Indian coffee',40,'beverage',True),('Buttermilk','Chilled spiced buttermilk',30,'beverage',True)]},
            {'meta': {'name': 'Dragon Palace', 'cuisine': 'Chinese', 'address': '78 Bharathi Road, Tiruppur', 'rating': 4.1, 'delivery_time': 35, 'min_order': 200},
             'menu': [('Veg Spring Rolls','Crispy rolls with vegetables',140,'starter',True),('Chicken Manchurian','Crispy chicken in manchurian sauce',220,'starter',False),('Veg Fried Rice','Wok-tossed rice with vegetables',160,'main',True),('Chicken Fried Rice','Rice with eggs and chicken',200,'main',False),('Paneer Schezwan Noodles','Noodles in fiery Schezwan sauce',180,'main',True),('Sweet Corn Soup','Creamy corn soup',100,'starter',True),('Honey Chilli Potato','Crispy potato in sweet-spicy sauce',160,'starter',True),('Lemon Ice Tea','Iced tea with lemon',80,'beverage',True)]},
            {'meta': {'name': "Mario's Pizza", 'cuisine': 'Pizza & Italian', 'address': '22 New Street, Tiruppur', 'rating': 4.6, 'delivery_time': 40, 'min_order': 250},
             'menu': [('Garlic Bread','Toasted baguette with herb butter',100,'starter',True),('Margherita Pizza','Classic pizza with mozzarella and basil',280,'main',True),('Pepperoni Pizza','Loaded with pepperoni',360,'main',False),('Paneer Tikka Pizza','Indian fusion pizza',320,'main',True),('Pasta Arrabbiata','Penne in spicy tomato sauce',220,'main',True),('Tiramisu','Classic Italian coffee dessert',150,'dessert',True),('Virgin Mojito','Mint lemon drink with soda',100,'beverage',True)]},
            {'meta': {'name': 'Biryani House', 'cuisine': 'Biryani & Kebabs', 'address': '5 Palladam Road, Tiruppur', 'rating': 4.7, 'delivery_time': 45, 'min_order': 180},
             'menu': [('Chicken Dum Biryani','Aromatic basmati with chicken',320,'main',False),('Veg Biryani','Fragrant rice with vegetables',220,'main',True),('Mutton Biryani','Tender mutton with aged basmati',380,'main',False),('Egg Biryani','Eggs layered with spiced rice',240,'main',False),('Hara Bhara Kebab','Spinach and peas patties',140,'starter',True),('Raita','Yogurt with cucumber and mint',60,'starter',True),('Phirni','Chilled rice pudding',90,'dessert',True),('Rose Milk','Chilled milk with rose essence',60,'beverage',True)]},
            {'meta': {'name': 'Burger Baron', 'cuisine': 'Burgers & Fast Food', 'address': '33 Perundurai Road, Tiruppur', 'rating': 4.2, 'delivery_time': 20, 'min_order': 120},
             'menu': [('Classic Veg Burger','Aloo tikki with fresh veggies',150,'main',True),('Zinger Chicken Burger','Spicy crispy chicken burger',200,'main',False),('Double Smash Burger','Two smashed patties with cheese',280,'main',False),('Crispy Corn Bites','Fried corn kernels',100,'starter',True),('Onion Rings','Beer-battered onion rings',120,'starter',True),('Waffle Fries','Crispy waffle-cut fries',100,'starter',True),('Chocolate Shake','Thick chocolate milkshake',140,'beverage',True),('Brownie Sundae','Warm brownie with ice cream',160,'dessert',True)]},
        ]

        for r in restaurants:
            rest, created = Restaurant.objects.get_or_create(name=r['meta']['name'], defaults=r['meta'])
            if created:
                for (name, desc, price, cat, is_veg) in r['menu']:
                    FoodItem.objects.create(restaurant=rest, name=name, description=desc, price=price, category=cat, is_veg=is_veg)
                self.stdout.write(f'Created: {rest.name}')

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
