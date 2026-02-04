from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


ROOM_CHOICES = [
    ('Single', 'Single'),
    ('Double', 'Double'),
    ('Suite',  'Suite'),
]


ROOM_CAPACITY = {'Single': 5, 'Double': 3, 'Suite': 2}
ROOM_PRICE = {'Single': 1000, 'Double': 1800, 'Suite': 3000}



#create a model for reservations
class Reservation(models.Model):
    
    #reserve status 
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )

    #each reservation for one user , one user many reservations
    #if user deleted , reservation deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=20)  # فقط نام اتاق
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True) # time of reserve

    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    payment_deadline = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.payment_deadline:
            self.payment_deadline = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs) #save reserve in database

    @property
    def nights(self):
        return (self.checkout_date - self.checkin_date).days

    @property
    def total_price(self):
        return self.nights * ROOM_PRICE.get(self.room_type, 0)

    @property
    def is_payment_pending(self):
        return self.status == "pending" and not self.is_paid and timezone.now() < self.payment_deadline

    @property
    def is_payment_expired(self):
        return self.status == "pending" and not self.is_paid and timezone.now() >= self.payment_deadline

    def __str__(self):
        return f"{self.user.first_name} - {self.room_type} ({self.checkin_date} to {self.checkout_date})"
