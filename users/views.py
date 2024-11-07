from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .forms import ProfileEditForm
from services.models import Service
from django.utils import timezone
from bookings.models import Booking
from notifications.models import Notification
from django.contrib import messages
from django.contrib.auth import logout


def home(request):
    return render(request, 'core/home.html') 

# Vista basada en clase para registro
class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        if not (user.is_company or user.is_client):
            user.is_client = True
        user.save()
        login(self.request, user)
        messages.success(self.request, "¡Registro exitoso! Bienvenido a la plataforma.")
        return redirect('profile')

# Vista para el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Has iniciado sesión exitosamente.")
            return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, "Credenciales incorrectas. Inténtalo de nuevo.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('home')

# Vista para el perfil de usuario (requiere inicio de sesión)
@login_required
def profile_view(request):
    user = request.user
    
    if user.is_company:
        # Lógica para el perfil de la empresa
        offered_services = user.services.all()
        company_bookings = Booking.objects.filter(service__in=offered_services).order_by('-date')
        pending_count = company_bookings.filter(status='pending').count()
        notifications = Notification.objects.filter(user=user, is_read=False)
        print("Notificaciones no leídas (empresa):", notifications)

        return render(request, 'users/profile_company.html', {
            'user': user,
            'offered_services': offered_services,
            'company_bookings': company_bookings,
            'pending_count': pending_count,
            'notifications': notifications,
        })
    else:
        # Lógica para el perfil del cliente
        past_bookings = user.client_bookings.filter(date__lt=timezone.now())
        
        # Filtrar las notificaciones no leídas
        notifications = Notification.objects.filter(user=user, is_read=False)
        print("Notificaciones no leídas (cliente):", notifications)

        # Verificar si hay duplicados de notificación y eliminarlos
        unique_notifications = []
        seen_messages = set()
        for notification in notifications:
            if notification.message not in seen_messages:
                unique_notifications.append(notification)
                seen_messages.add(notification.message)

        return render(request, 'users/profile_client.html', {
            'user': user,
            'past_bookings': past_bookings,
            'notifications': unique_notifications,
        })

    
@login_required
def dashboard_view(request):
    user = request.user
    if user.is_company:
        company_services = Service.objects.filter(provider=user)
        pending_bookings = Booking.objects.filter(service__in=company_services, status='pending')
        pending_count = pending_bookings.count()

        return render(request, 'users/dashboard_company.html', {
            'pending_bookings': pending_bookings,
            'pending_count': pending_count,
            'notifications': Notification.objects.filter(user=user, is_read=False),
            'user': user,
        })
    else:
        active_bookings = user.client_bookings.filter(date__gte=timezone.now(), status='confirmed')
        recommended_services = Service.objects.exclude(provider=user)
        
        # Sin filtro `is_read` para mostrar todas las notificaciones
        return render(request, 'users/dashboard_client.html', {
            'active_bookings': active_bookings,
            'recommended_services': recommended_services,
            'notifications': Notification.objects.filter(user=user),
            'user': user,
        })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Información actualizada exitosamente.")
            return redirect('profile')
        else:
            messages.error(request, "Hubo un error al actualizar el perfil. Inténtalo de nuevo.") 
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})