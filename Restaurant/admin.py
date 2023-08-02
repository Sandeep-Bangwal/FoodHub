from django.contrib import admin
from .models import *

@admin.register(rest_registration)
class rest_registrationAdmin(admin.ModelAdmin):
    list_display = ['user','rest_id','rest_name','slug', 'owner_name', 'food_type' ]


@admin.register(menus)
class MenusAdmin(admin.ModelAdmin):
    list_display = ['rest_id','food_name','cat', 'img', 'price', 'description' ]