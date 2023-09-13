from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Orders)
class ordersAdmin(admin.ModelAdmin):
    list_display = ['cart', 'total_amounts','razorpay_payment_id','razorpay_order_id','status','address','createAt'] 

@admin.register(order_address)
class ordersAdmin(admin.ModelAdmin):
    list_display = ['uid','user']  

@admin.register(order_address_details)
class ordersAdmin(admin.ModelAdmin):
    list_display = ['uid','order_add_id','customer_name','mob_no','line','city','state','zipCode'] 