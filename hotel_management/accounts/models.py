from django.contrib.auth.models import AbstractUser # djnago base class for custom user model
from django.db import models
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

#if we had just User we cound not change username 
class CustomUser(AbstractUser):
    
    usename= None # we dont need username that why we used abstractuser 
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'phone_number'#users will login wiht phone number  
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    #print in shall 
    
    

class EmailOTP(models.Model):
    #one to many realationship , one otp one user but one user many otp
    user = models.ForeignKey(settings.AUTH_USER_MODEL)# connect Customuser instead of User
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
     
     
     #otp has 5 min , this checks if its still valid
    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)
