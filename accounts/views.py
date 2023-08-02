from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from datetime import datetime, timedelta
import random 

#sent OTP in user email id 
def sent(email, otp):
     send_mail(
         'One Time Password',
         'Please use the verification code below to sign in. \n'+otp+'\nIf you did not request this, you can ignore this email. \n'+'\nThanks,'+'\n Team \n Suvidha & sandeep',
         'foodorder650@gmail.com',
         [email],
         fail_silently=False,
        )
     return None

#creating a user signup with sent otp for customer 
def hendle_signup(request):
        if request.method == 'POST':
            name =  request.POST['name']
            phone_no =  request.POST['phone_no']
            email =  request.POST['email']
            chek_user  = User.objects.filter(email=email).first()
            if chek_user is not None:
                 messages.error(request,"Email id alredy registered")
                 return render(request, 'accounts/signup.html')
            otp = str(random.randint(1000, 9999))
            add_user = User(email = email, full_name = name, mobile_no = phone_no, otp = otp, user_type = User.CUSTOMER).save()
            request.session['email'] = email
            sent(email, otp)

            #start timer for otp enter the before time 60
            otp_expiry = datetime.now() + timedelta(seconds=60)
            request.session['otp_expiry'] = otp_expiry.strftime('%Y-%m-%d %H:%M:%S')
            return redirect("verify_otp")
        else:
          return render(request, 'accounts/signup.html')
   
# log in view and sent OTP to agin login attemp 
def hendle_login(request):
     if request.method == 'POST':
        email = request.POST.get('email')

        user = User.objects.filter(email= email).first()
        if user is None:
            messages.error(request,"Your email id does not exist")
            return render(request, 'accounts/login.html')
        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        sent(email, otp)

        #start timer for otp enter the before time 60
        otp_expiry = datetime.now() + timedelta(seconds=60)
        request.session['otp_expiry'] = otp_expiry.strftime('%Y-%m-%d %H:%M:%S')
        request.session['email'] = email
        return redirect("verify_otp")
     else:
      print(datetime.now())
      return render(request, 'accounts/login.html')

#verify OTP view for OTP verifications 
def verify_otp(request):
    if request.method == 'POST':
        Email = request.POST.get('email')
        otp = request.POST.get('otp')

        try:
            user = User.objects.get(email= Email)
        except User.DoesNotExist:
            messages.error(request,"User does not exist")
            return render(request, 'accounts/otp.html')
        
        #chek the OTP expired
        now = datetime.now()
        if str(now) > request.session['otp_expiry'] :
            messages.error(request, 'OTP has expired')
            return render(request, 'accounts/otp.html')
        
        if otp == user.otp:
            login(request, user)
            if user.user_type == 'customer':
             return redirect("/")
            else:
              return render(request, 'restaurant/addRestaurant.html')  
        else:
            messages.error(request,"OTP does not match")
            return redirect("verify_otp")
    else:
        return render(request, 'accounts/otp.html')
    
# log out
def hendle_logout(request):
    logout(request)
    return redirect("login")

# creating accounts for resturants
def restaurant_signup(request):
        if request.method == 'POST':
            name = request.POST['name']
            phone_no = request.POST['phone_no']
            email = request.POST['email']

            chek_user  = User.objects.filter(email=email).first()
            if chek_user is not None:
                messages.error(request,"Email id alredy registered")
                return render(request, 'accounts/signup.html')
            
            # genreting the otp
            otp = str(random.randint(1000, 9999))
            add_user = User(email = email, full_name = name, mobile_no = phone_no, otp = otp, user_type = User.RESTAURANT).save()
            request.session['email'] = email
            sent(email, otp)
           
            #start timer for otp enter the before time 60
            otp_expiry = datetime.now() + timedelta(seconds=60)
            request.session['otp_expiry'] = otp_expiry.strftime('%Y-%m-%d %H:%M:%S')
            return redirect("verify_otp")
        else:
         return render(request, 'accounts/signup.html')
        
# resent otp
def resent_otp(request):
     otp = str(random.randint(1000, 9999))
     again_sent = User.objects.filter(email=request.session['email']).first()
     again_sent.otp = otp
     again_sent.save()
     sent(request.session['email'], otp)
     otp_expiry = datetime.now() + timedelta(seconds=60)
     request.session['otp_expiry'] = otp_expiry.strftime('%Y-%m-%d %H:%M:%S')
     return redirect("verify_otp")  