from django.db import models
from accounts.models import User
from autoslug import AutoSlugField
import uuid


# Create your models here.
class rest_registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rest_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rest_name= models.CharField(max_length=60)
    slug = AutoSlugField(populate_from='rest_name', unique=True, null=True, default=None)
    owner_name = models.CharField(max_length=40)
    address= models.CharField(max_length=50)
    zip = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    open =models.TimeField()
    close = models.TimeField()
    days = models.CharField(max_length=100)
    img = models.ImageField(upload_to="resturant_img")
    food_type = models.CharField(max_length=100)
    rating = models.DecimalField(blank=True, max_digits=2, decimal_places=1, default=1.0)
 
class menus(models.Model):
    rest_id = models.ForeignKey(rest_registration, on_delete=models.CASCADE, related_name="menu")  
    food_name = models.CharField(max_length=100)
    cat = models.CharField(max_length=50)  
    img = models.ImageField(upload_to="menus")
    price = models.IntegerField()
    description = models.TextField()


