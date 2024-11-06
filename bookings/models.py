# bookings/models.py
from django.db import models
from services.models import Service
from users.models import CustomUser
from django.utils import timezone

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="client_bookings")
    date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed')], default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.service.name} on {self.date}"

    @property
    def is_active(self):
        return self.date >= timezone.now()  # Define una reserva como activa si la fecha es futura
