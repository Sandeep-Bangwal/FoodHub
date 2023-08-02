from django.contrib.auth.models import  BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, mobile_no, otp, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), full_name=full_name, mobile_no=mobile_no, otp=otp, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, mobile_no, otp, password=None):
        user = self.create_user(
            email,
            password=password,
            full_name= full_name,
            mobile_no = mobile_no,
            otp= otp,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
        
        # return self.create_user(email, full_name, mobile_no, otp, password)