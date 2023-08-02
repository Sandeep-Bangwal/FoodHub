from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('searchcity', views.searchCity, name='city'),
    path('restaurant/<slug>', views.restaurant, name='restaurant'),
    path('cart', views.cart, name='cart'),
    path('remove/<uid>', views.remove_items, name='remove'),
    path('add_to_card/<int:id>', views.add_to_card, name='add_to_card'),
    path('chek_out', views.chek_out, name='chek_out'),
    path('success', views.payment_success, name='success'),
    path('view_orders', views.view_orders, name='view_orders'),
    path('Ordertrack/<uid>', views.Ordertrack, name='Ordertrack'),

]