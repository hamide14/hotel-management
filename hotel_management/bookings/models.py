from django.db import models
from django.conf import settings
from rooms.models import RoomType
from django.utils import timezone
from datetime import timedelta

class Reservation(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

  
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    payment_deadline = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.payment_deadline:
            self.payment_deadline = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    @property
    def is_payment_pending(self):
        return self.status == "pending" and not self.is_paid and timezone.now() < self.payment_deadline

    @property
    def is_payment_expired(self):
        return self.status == "pending" and not self.is_paid and timezone.now() >= self.payment_deadline

    def __str__(self):
        return f"{self.user.first_name} - {self.room_type.name} ({self.checkin_date} to {self.checkout_date})"
