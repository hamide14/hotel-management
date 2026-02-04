from django import forms
from .models import Reservation



#our list for rooms (value , display)
ROOM_CHOICES = [
    ('Single', 'Single'),
    ('Double', 'Double'),
    ('Suite',  'Suite'),
]


# this form directly linked to Reservation model
class ReservationForm(forms.ModelForm):
    room_type = forms.ChoiceField(choices=ROOM_CHOICES, label="Room Type")

    class Meta:
        model = Reservation
        fields = ['room_type', 'checkin_date', 'checkout_date', 'guests']
        #what kind of input for fields in html
        widgets = {
            'checkin_date': forms.DateInput(attrs={'type': 'date'}),    #calenders
            'checkout_date': forms.DateInput(attrs={'type': 'date'}),
        }
