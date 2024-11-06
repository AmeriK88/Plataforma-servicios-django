from django.db import models
from services.models import Service
from users.models import CustomUser

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.client.username} - {self.service.name} on {self.date}"
