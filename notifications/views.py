# notifications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification

def notification_list(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    print("Notificaciones en la lista:", notifications)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})


def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    return render(request, 'notifications/notification_detail.html', {'notification': notification})

def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    return redirect('notification_list')
 



