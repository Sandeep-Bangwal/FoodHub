from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager



class User(AbstractBaseUser):
    CUSTOMER = 'customer'
    RESTAURANT  = 'restaurant'
    USER_TYPE_CHOICES = (
        (CUSTOMER, 'Customer'),
        ( RESTAURANT , 'restaurant'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=12)
    otp = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'mobile_no', 'otp']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin




