# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    path('new/<int:service_id>/', views.booking_create, name='booking_create'),
]
