# notifications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification

def notification_list(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    return render(request, 'notifications/notification_detail.html', {'notification': notification})

def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')

