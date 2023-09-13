from django.urls import path
from . import views

urlpatterns = [
    path('chek_out', views.chek_out, name='chek_out'),
    path('payment', views.payment, name='payment'),
    path('success', views.payment_success, name='success'),
    path('view_orders', views.view_orders, name='view_orders'),
    path('Ordertrack/<uid>', views.Ordertrack, name='Ordertrack'),

]