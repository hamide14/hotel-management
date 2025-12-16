from django import forms
from .models import Reservation
from rooms.models import RoomType

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room_type', 'checkin_date', 'checkout_date', 'guests']
        widgets = {
            'checkin_date': forms.DateInput(attrs={'type': 'date'}),
            'checkout_date': forms.DateInput(attrs={'type': 'date'}),
        }
