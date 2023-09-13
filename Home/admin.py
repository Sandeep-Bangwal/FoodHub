from django.contrib import admin
from .models import *

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code','is_expired','min_amount','discount']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','is_paid','coupon']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','food']    
       


