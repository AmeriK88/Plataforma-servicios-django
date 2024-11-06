# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm
from services.models import Service
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from django.db import IntegrityError
from django.contrib import messages


@login_required
def booking_list(request):
    """ Muestra la lista de todas las reservas del usuario actual """
    # Filtra solo las reservas del usuario autenticado
    bookings = Booking.objects.filter(user=request.user)  
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    """ Muestra los detalles de una reserva específica """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)  # Asegura que solo el usuario autenticado pueda ver sus reservas
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def booking_create(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  
            booking.service = service    
            booking.status = 'pending'   #
            booking.save()
            return redirect('dashboard')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form, 'service': service})

@login_required
def confirm_booking(request, pk):
    try:
        booking = get_object_or_404(Booking, pk=pk)
        
        # Verificación de que el usuario sea el proveedor del servicio
        if request.user == booking.service.provider:
            # Confirmamos que el servicio y usuario referenciados existen
            if booking.service and booking.user:
                booking.status = 'confirmed'
                booking.save()
                
                # Notificación de confirmación para el cliente
                Notification.objects.create(
                    user=booking.user,
                    message=f"Tu reserva para {booking.service.name} ha sido confirmada."
                )
                messages.success(request, "Reserva confirmada exitosamente.")
            else:
                messages.error(request, "Error: El servicio o usuario asociado no existe.")
        else:
            messages.error(request, "No tienes permiso para confirmar esta reserva.")
            
    except IntegrityError:
        messages.error(request, "Error al confirmar la reserva debido a una restricción de clave foránea.")
    
    return redirect('dashboard')

@login_required
def reject_booking(request, pk):
    try:
        booking = get_object_or_404(Booking, pk=pk)
        
        # Verificación de que el usuario sea el proveedor del servicio
        if request.user == booking.service.provider:
            # Confirmamos que el servicio y usuario referenciados existen
            if booking.service and booking.user:
                booking.status = 'rejected'
                booking.save()
                
                # Notificación de rechazo para el cliente
                Notification.objects.create(
                    user=booking.user,
                    message=f"Lamentablemente, tu reserva para {booking.service.name} ha sido rechazada."
                )
                messages.success(request, "Reserva rechazada exitosamente.")
            else:
                messages.error(request, "Error: El servicio o usuario asociado no existe.")
        else:
            messages.error(request, "No tienes permiso para rechazar esta reserva.")
            
    except IntegrityError:
        messages.error(request, "Error al rechazar la reserva debido a una restricción de clave foránea.")
    
    return redirect('dashboard')
