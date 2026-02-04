from django import forms
from .models import Reservation

ROOM_CHOICES = [
    ('Single', 'Single'),
    ('Double', 'Double'),
    ('Suite',  'Suite'),
]



class ReservationForm(forms.ModelForm):
    room_type = forms.ChoiceField(choices=ROOM_CHOICES, label="Room Type")

    class Meta:
        model = Reservation
        fields = ['room_type', 'checkin_date', 'checkout_date', 'guests']
        widgets = {
            'checkin_date': forms.DateInput(attrs={'type': 'date'}),
            'checkout_date': forms.DateInput(attrs={'type': 'date'}),
        }
