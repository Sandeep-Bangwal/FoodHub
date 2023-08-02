from django.shortcuts import render, redirect
from .models import rest_registration, menus
from accounts.models import User
from django.contrib.auth.decorators import login_required
from Home.models import *
from django.db.models import Sum


# Create your views here.
def add_restaurant(request):
    return render(request, 'restaurant/addRestaurant.html')

#resturnat registration 
@login_required(login_url="login")
def registration(request):
    if request.method == 'POST':
     restaurant_name= request.POST['name']
     Owner_name= request.POST['Owner_name']
     address= request.POST['address']
     City= request.POST['City']
     state= request.POST['state']
     Zip= request.POST['Zip']
     open= request.POST['open']
     close= request.POST['close']
     days= request.POST.getlist('days')
     food_type= request.POST.getlist('food_type')
     
     img= request.FILES['img']

     register = rest_registration.objects.create(
        user = User(id=request.user.id),
        rest_name = restaurant_name,
        owner_name= Owner_name,
        address= address,
        city= City,
        zip=Zip,
        state=state,
        open=open, 
        close= close,
        days= days,
        food_type =food_type,
        img = img,
     )
     return redirect('deshboard')
    else:
     return render(request, 'restaurant/registration.html')


# deshboard for  restaurant
@login_required(login_url="login")
def deshboard(request):
   getid = rest_registration.objects.get(user = request.user.id)
   # calculate the total order 
   TotalOrders =Orders.objects.filter(cart__cartItems__food__rest_id = getid.rest_id).count()
    # calculate the total pending order 
   PendingOrders =Orders.objects.filter(cart__cartItems__food__rest_id = getid.rest_id).exclude(status = "delivered").count()
    # calculate the total order complete 
   TotalOrdersFulfilled  = Orders.objects.filter(cart__cartItems__food__rest_id = getid.rest_id, status = "delivered").count()

   # ordre list 
   order_recevie =Orders.objects.filter(cart__cartItems__food__rest_id = getid.rest_id).values('cart__cartItems__food__img', 'cart__cartItems__food__food_name','total_amounts', 'uid', 'status')
   context = {
      'order_recevie':order_recevie,
      'TotalOrders':TotalOrders,
      'TotalOrdersFulfilled':TotalOrdersFulfilled,
      'PendingOrders': PendingOrders
   }
        
   return render(request, 'restaurant/deshboard.html', context)

#deshboard for adding menus for restaurant
@login_required(login_url="login")
def CreateMenus(request):
     """
     Get the user id from resturant table
     """
     getid = rest_registration.objects.get(user = request.user.id)
     if request.method == 'POST':
       food_title = request.POST.get('name')
       categories= request.POST.get('categories')
       img= request.FILES['img']
       price= request.POST.get('price')
       desc= request.POST.get('desc')
       add_menu = menus.objects.create(rest_id = rest_registration(rest_id=getid.rest_id), food_name = food_title, cat=categories, img=img, price=price, description=desc)
       return render(request, 'restaurant/addMenus.html')
     else:
        dis = menus.objects.filter(rest_id=getid.rest_id)
        return render(request, 'restaurant/addMenus.html',{'dis': dis})
     
# order display    
def OdersReceived(request):
   getid = rest_registration.objects.get(user = request.user.id)
   order_recevie =Orders.objects.filter(cart__cartItems__food__rest_id = getid.rest_id).values('cart__cartItems__food__food_name','total_amounts', 'uid', 'status')
   context = {
      'order_recevie':order_recevie,
   }
   return render(request, 'restaurant/orderReceive.html', context)  

# Update the orders status 
def update_status(request, uid):
   if request.method == 'POST':
      status = request.POST['status']
      
      # get the order id (uid)
      updates = Orders.objects.get(uid = uid)
      updates.status = status 
      updates.save()
       
      return redirect('OdersReceived')
   