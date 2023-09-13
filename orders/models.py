from django.db import models
from Home.models import BaseModel, Cart, CartItem
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder

class order_address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')  
      
class order_address_details(BaseModel):
    order_add_id = models.ForeignKey(order_address, on_delete=models.CASCADE, related_name='address')
    customer_name = models.CharField(max_length=50)
    mob_no = models.CharField(max_length=12)
    line = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100) 
    zipCode = models.IntegerField()
    
# Orders model relationship with cart
class Orders(BaseModel):
    order_status = (
    ("Order Recieved", "Order Recieved"),
    ("Baking", "Baking"),
    ("Baked", "Baked"),
    ("Out for delivery", "Out for delivery"),
    ("delivered ", "delivered ")   
    )
    
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_cart')
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)  
    razorpay_order_id = models.CharField(max_length=100, unique=True) 
    total_amounts = models.IntegerField(default=0)
    address= models.ForeignKey(order_address_details, on_delete=models.CASCADE, blank=True)
    status = models.CharField(max_length=50, default="Order Recieved", choices=order_status)
    createAt = models.DateField(auto_now_add=True, blank=True)

    # static method for get the order details its use iin channels
    @staticmethod
    def give_order_details(order_id):
        instance = Orders.objects.filter(uid=order_id).first()
        """
        this is used for hendel error uid is not json serilizer error 
        """
        uid = json.dumps(instance.uid, cls=DjangoJSONEncoder)
        data  = {}
        data['order_id'] = uid
      
        data['status'] = instance.status

        progress_percentage = 20
        if instance.status == 'Order Recieved':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for delivery':
            progress_percentage = 80
        elif instance.status == 'delivered':
            progress_percentage = 100
            
        data['progress'] = progress_percentage
        
        return data
        

# singles for real time order status progress tracking
@receiver(post_save, sender=Orders)
def order_status_handler(sender, instance,created , **kwargs):
    
    if not created:
        channel_layer = get_channel_layer()
        uid = json.dumps(instance.uid, cls=DjangoJSONEncoder)
        data  = {}
        data['order_id'] = uid
        data['status'] = instance.status
        progress_percentage = 20
        if instance.status == 'Order Recieved':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for delivery':
            progress_percentage = 80
        elif instance.status == 'delivered':
            progress_percentage = 100
    
        
        data['progress'] = progress_percentage
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.uid,{
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )


# singles for new order created notification to sent seller deshboard
@receiver(post_save, sender = Orders) 
def order_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        data ={}
        user = User.objects.get(id=instance.cart.cartItems.first().food.rest_id.user.id)
        count = Orders.objects.filter(cart__cartItems__food__rest_id__user = user.id).count()
        data['count'] = count
        async_to_sync(channel_layer.group_send)(
            'notification' , {
                'type': 'Order.Notification',
                'value': json.dumps(data)
            }
        )