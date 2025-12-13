from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, mobaile , email , first_name , last_name , password = None):
        if not mobile:
            raise ValueError("شماره موبایل الزامی است")
        user = self.model(
            mobile = 
        )
                
            
        