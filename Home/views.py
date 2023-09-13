from django.shortcuts import render, HttpResponse
from Restaurant.models import rest_registration, menus
from datetime import datetime, time,  timedelta
from django.http import HttpResponseRedirect
from .models import *
from orders.models import Orders
from django.db.models import Sum
from django.contrib import messages
import razorpay
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required


#index page get method for render the index page
def home(request):
    return render(request, 'home/index.html')


#searched resturants results 
def searchCity(request):
    
    # search the restaurant base on city
    if request.method == 'POST':
       search = request.POST.get('search')
       result =  request.session['search'] = search
       restaurant_list = rest_registration.objects.annotate(
          search=SearchVector('address', 'state', 'city')).filter(search__icontains=result)
       count = restaurant_list.count()
       return render(request, 'home/city.html', {'restaurant': restaurant_list, 'restaurant_count': count})

    # sort by the rating, indian, fast food etc restaurant   
    if request.method == 'GET':
            sort_by = request.GET.get('sort_by')
            sort_by_food = request.GET.get('sort_by_food')
            # sort by the rating
            if sort_by == 'rating':
                restaurant_list = rest_registration.objects.annotate(
                search=SearchVector('address', 'state', 'city')).filter(search__icontains= request.session['search']).order_by('-rating')
                count = restaurant_list.count()
                return render(request, 'home/city.html', {'restaurant': restaurant_list, 'restaurant_count': count}) 
            # sort by the Relevance
            elif sort_by == 'Relevance':
                restaurant_list = rest_registration.objects.annotate(
                    search=SearchVector('address', 'state', 'city')).filter(search__icontains= request.session['search'])  
                count = restaurant_list.count()
                return render(request, 'home/city.html', {'restaurant': restaurant_list, 'restaurant_count': count})
            else:
                # filter by the food types like fast foods, indains etc
                restaurant_list = rest_registration.objects.annotate(
                search=SearchVector('address', 'state', 'city')).filter(search__icontains= request.session['search'], food_type__icontains = sort_by_food).order_by('food_type')  
                count = restaurant_list.count()
                return render(request, 'home/city.html', {'restaurant': restaurant_list, 'restaurant_count': count})      
    return render(request, 'home/city.html', {'restaurant': restaurant_list})

# calucate the Restaurant close time 
def get_Restaurant_close_time(close):
    current_time = datetime.now().time()
    if current_time > close:
        remaining_time = timedelta(days=1) - (datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), close))
    else:
        remaining_time = datetime.combine(datetime.today(), close) - datetime.combine(datetime.today(), current_time)
   
    hours = remaining_time.seconds // 3600
    minutes = (remaining_time.seconds % 3600) // 60
    seconds = remaining_time.seconds % 60

    # Format remaining time or display closed message
    if current_time > close:
        remaining_time = "closed"
    elif hours == 0 and minutes == 0:
        remaining_time = f"Close in {seconds} seconds"
    elif hours == 0:   
        remaining_time = f"Close in {minutes} minutes {seconds} seconds" 
    else:
        remaining_time = f"Close in {hours} hours {minutes} minutes {seconds} seconds"

    return remaining_time

def restaurant(request, slug):
    view_rest = rest_registration.objects.get(slug = slug)
    food_list = menus.objects.filter(rest_id = view_rest.rest_id)
    food_types = eval(view_rest.food_type)

    """
    get the restaurant close time 
    using the get_Restaurant_close_time method pass the close parameter form database
    """
    close = view_rest.close
    remaining_time = get_Restaurant_close_time(close)
  
    context = {
        'view_rest':view_rest,
        'menus':food_list,
        'coupon': Coupon.objects.all(),
        'remaining_time':remaining_time,
        'food_types':  food_types 
    }
    return render(request, 'home/view.html', context)

# add to the cart 
@login_required(login_url="login")
def add_to_card(request,id):
    food_items = menus.objects.get(id = id)
    user = request.user.id
    """
    if the card object is exit and not exit then 
    create the new carts user objects 
    """
    carts, _ = Cart.objects.get_or_create(user = User(id = user), is_paid = False) 
    cart_items = CartItem.objects.create(cart = carts, food = food_items)

    # Cart count 
    request.session['cart_counts'] = CartItem.objects.filter(cart__user = request.user.id, cart__is_paid=False ).count()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#display the carts items added by the users
def cart(request):

    try:
     cart_obj = Cart.objects.get(is_paid=False, user=request.user.id)
     """
     if the all card items is deleted but user objects is exit in the cart_obj
     """
     if CartItem.objects.filter(cart__user = request.user.id, cart__is_paid=False ).count() == 0:
        request.session['cart_counts'] = 0
        return render(request, 'home/cart.html', {'error':'Your Cart is Empty'})
     # Cart object exists, continue with further processing
    except Cart.DoesNotExist:
        request.session['cart_counts'] = CartItem.objects.filter(cart__user = request.user.id, cart__is_paid=False ).count()
        return render(request, 'home/cart.html', {'error':'Your Cart is Empty'})
    
    
    totals = CartItem.objects.filter(cart__user = request.user.id, cart__is_paid = False).aggregate(sum =Sum("food__price"))
    sum_price = totals["sum"]

    # user id input the Coupon code 
    if request.method == 'POST':
        Coupon_code = request.POST.get('Coupon_code')
        coupon_get = Coupon.objects.filter(coupon_code = Coupon_code).first()
        # coupon code inter is not match
        if not coupon_get:
          messages.error(request,"Invaild Coupon")
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        # coupon code is alredy exit 
        if cart_obj.coupon:
          messages.error(request,"Coupon already exits")
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        # all the condition is true the save the coupon code 
        cart_obj.coupon = coupon_get
        cart_obj.save()
        messages.success(request,"Coupon applied")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    price = {}

    if cart_obj.coupon and sum_price >= cart_obj.coupon.min_amount:
        price['total'] = sum_price - cart_obj.coupon.discount

    else:
       price['total']  = sum_price

    print(price['total']) 
    
    context = {
        'cart_items': CartItem.objects.filter(cart__user = request.user.id, cart__is_paid = False),
        'totals': totals,
        'cart_obj':cart_obj,
        'price':price
    }
    return render(request, 'home/cart.html', context)


#Remove the items form the card
def remove_items(request, uid):
  remove = CartItem.objects.filter(uid = uid).delete()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

