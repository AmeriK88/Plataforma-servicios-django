# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm
from services.models import Service
from django.contrib.auth.decorators import login_required

@login_required
def booking_list(request):
    """ Muestra la lista de todas las reservas del usuario actual """
    bookings = Booking.objects.filter(user=request.user)  # Filtra solo las reservas del usuario autenticado
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    """ Muestra los detalles de una reserva específica """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)  # Asegura que solo el usuario autenticado pueda ver sus reservas
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def booking_create(request, service_id):
    """ Permite al usuario crear una nueva reserva para un servicio específico """
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.user = request.user
            booking.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'form': form, 'service': service})
