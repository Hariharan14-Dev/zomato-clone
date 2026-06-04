from django.contrib import admin
from django.urls import path
from food import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:pk>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
