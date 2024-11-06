from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    # Agrega related_name para evitar conflictos con el modelo auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Cambia a un related_name único
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Cambia a un related_name único
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
