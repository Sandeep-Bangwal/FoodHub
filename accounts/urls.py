from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.hendle_signup, name='signup'),
    path('login', views.hendle_login, name='login'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('sent', views.sent, name='sent'),
    path('logout', views.hendle_logout, name='logout'),
    path('resent_otp', views.resent_otp, name='resent_otp'),
    path('restaurant_signup', views.restaurant_signup, name='restaurant_signup'),

]