from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from .models import *
from django.contrib import messages
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required

#chek out page
@login_required(login_url="login")
def chek_out(request):
    price = request.GET['price']
    dis = request.GET['dis']
    finalAmount = request.GET['finalAm']
      
    if request.method == 'POST':
        name = request.POST['name']
        mobileNumber = request.POST['mobileNumber']
        Address = request.POST['Address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        
        user , _ = order_address.objects.get_or_create(user = User(id =request.user.id))
        createAddress = order_address_details(order_add_id = user, customer_name = name,mob_no=mobileNumber, line=Address, city =city, state = state, zipCode = zip)
        createAddress.save()
        if createAddress:
         messages.success(request,"Adrress created")
        else:
            messages.error(request, "Not") 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    # Razorpay payment 
    client = razorpay.Client(auth=(settings.SECRET_KEY1, settings.SECRET_KEY))
    data = { "amount": int(finalAmount)*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
  
    cart_obj = Cart.objects.get(is_paid=False, user=request.user.id)

    # save the user paymet id into order table
    order = Orders.objects.create(cart = cart_obj, razorpay_order_id = payment['id'], address=order_address_details(uid = '5f64b966-31a6-4e4f-9dbc-07d18ad44355'))
       
    getAddress = order_address_details.objects.filter(order_add_id__user = request.user.id)    
    context = {
        'price':price,
        'Discount':dis,
        'finalAmount':finalAmount,
        'getAddress':getAddress,
        'payment':payment,
    
    }    
    return render(request, 'orders/chekout.html', context)

def payment(request):
    return redirect("success")

def payment_success(request):
    
    """
    Payment is success the update the order table 
    to save the more information like the order id, amounts
    """     
    order_id = request.GET.get('order_id')
    amount = request.GET.get('amount')
    
    # change the paid False to True in card models
    cart = Cart.objects.filter(user = request.user.id).update(is_paid = True)
   
    obj = Orders.objects.filter(razorpay_order_id = order_id).update(razorpay_payment_id= request.GET.get('payment_id'), total_amounts = amount)
    response = "<h1>Payment is successfully processed.<a href='/orders/view_orders'>view order</a> to continue...</h1> "
    return HttpResponse(response)

    


# view the orders 
def view_orders(request):
    orders = Orders.objects.select_related('cart', 'cart__cartItems__food').filter(
        cart__is_paid=True, cart__user=request.user.id
    ).values(
        'cart__cartItems__food__food_name',
        'cart__cartItems__food__price',
        'cart__is_paid',
        'total_amounts',
        'razorpay_order_id',
        'cart__cartItems__food__img',
        'uid',
    )

    return render(request, 'orders/orders.html',{'orders':orders })

# order tacking
def Ordertrack(request, uid):
    return render(request, 'orders/OrderTrack.html', {'order_id':uid})