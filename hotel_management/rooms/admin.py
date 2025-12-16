from django.contrib import admin

# Register your models here.
# rooms/admin.py
from django.contrib import admin
from .models import RoomType

admin.site.register(RoomType)
