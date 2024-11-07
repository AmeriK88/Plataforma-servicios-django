# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm
from services.models import Service
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from django.db import IntegrityError
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)

@login_required
def booking_list(request):
    """ Muestra la lista de todas las reservas del usuario actual """
    bookings = Booking.objects.filter(user=request.user)  
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    """ Muestra los detalles de una reserva específica """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
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
            booking.status = 'pending'
            booking.save()
            messages.success(request, "Reserva creada exitosamente.")
            return redirect('dashboard')
        else:
            messages.error(request, "Hubo un error al crear la reserva. Inténtalo de nuevo.")
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form, 'service': service})

@login_required
def confirm_booking(request, pk):
    try:
        booking = get_object_or_404(Booking, pk=pk)
        if request.user == booking.service.provider:
            if booking.service and booking.user:
                booking.status = 'confirmed'
                booking.save()
                
                # Verificar si ya existe una notificación de confirmación para esta reserva
                if not Notification.objects.filter(user=booking.user, message__contains=f"Tu reserva para {booking.service.name} ha sido confirmada.").exists():
                    Notification.objects.create(
                        user=booking.user,
                        message=f"Tu reserva para {booking.service.name} ha sido confirmada."
                    )
                    messages.success(request, "Reserva confirmada exitosamente.")
                else:
                    messages.info(request, "La notificación de confirmación ya existe.")
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
        if request.user == booking.service.provider:
            if booking.service and booking.user:
                booking.status = 'rejected'
                booking.save()
                
                # Verificar si ya existe una notificación de rechazo para esta reserva
                if not Notification.objects.filter(user=booking.user, message__contains=f"Lamentablemente, tu reserva para {booking.service.name} ha sido rechazada.").exists():
                    Notification.objects.create(
                        user=booking.user,
                        message=f"Lamentablemente, tu reserva para {booking.service.name} ha sido rechazada."
                    )
                    messages.success(request, "Reserva rechazada exitosamente.")
                else:
                    messages.info(request, "La notificación de rechazo ya existe.")
            else:
                messages.error(request, "Error: El servicio o usuario asociado no existe.")
        else:
            messages.error(request, "No tienes permiso para rechazar esta reserva.")
            
    except IntegrityError:
        messages.error(request, "Error al rechazar la reserva debido a una restricción de clave foránea.")
    
    return redirect('dashboard')
