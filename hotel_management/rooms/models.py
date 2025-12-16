from django.db import models

class RoomType(models.Model):
    name = models.CharField(max_length=50)
    rooms = models.IntegerField() 
    price = models.DecimalField(max_digits=8, decimal_places=2 , default=1000)

    def __str__(self):
        return self.name

