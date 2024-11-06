# bookings/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date']  # Solo el campo 'date', excluyendo 'status'

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Añadir clases CSS al campo 'date'
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
