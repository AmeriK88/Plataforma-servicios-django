# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    path('new/', views.service_create, name='service_create'),
    path('<int:pk>/edit/', views.service_update, name='service_update'),
]
