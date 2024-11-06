from django.db import models
from users.models import CustomUser

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
