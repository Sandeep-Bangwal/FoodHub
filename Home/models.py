from django.db import models
from Restaurant.models import *
from accounts.models import User

 

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    class Meta:
        abstract = True 

# coupon code model
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=6)
    is_expired = models.BooleanField(default=False)
    min_amount = models.IntegerField(default=499)
    discount = models.IntegerField(default=100)

# cart model
class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True )
    
# cart item model with relationship with cart model
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cartItems')
    food = models.ForeignKey(menus, on_delete=models.SET_NULL, null=True)

      
