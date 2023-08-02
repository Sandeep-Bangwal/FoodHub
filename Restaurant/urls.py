from django.urls import path
from . import views

urlpatterns = [
    path('add_restaurant', views.add_restaurant, name='add_restaurant'),
    path('registration', views.registration, name='registration'),
    path('deshboard', views.deshboard, name='deshboard'),
    path('OdersReceived', views.OdersReceived, name='OdersReceived'),
    path('update_status/<uid>', views.update_status, name='update_status'),
    path('CreateMenus', views.CreateMenus, name='CreateMenus'),

]