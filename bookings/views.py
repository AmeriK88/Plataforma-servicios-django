# bookings/views.py
from django.shortcuts import render, get_object_or_404
from .models import Booking

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

def booking_create(request):
    # Lógica para crear una nueva reserva
    return render(request, 'bookings/booking_form.html')
