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
        return redirect('profile')

# Vista para el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Vista para el perfil de usuario (requiere inicio de sesión)
@login_required
def profile_view(request):
    user = request.user
    
    if user.is_company:
        offered_services = user.services.all()
        company_bookings = Booking.objects.filter(service__in=offered_services)
        return render(request, 'users/profile_company.html', {
            'user': user,
            'offered_services': offered_services,
            'company_bookings': company_bookings
        })
    else:
        # Para clientes, muestra el historial de reservas anteriores
        past_bookings = user.client_bookings.filter(date__lt=timezone.now())
        return render(request, 'users/profile_client.html', {
            'user': user,
            'past_bookings': past_bookings
        })
    
    
@login_required
def dashboard_view(request):
    user = request.user
    if user.is_company:
        company_services = Service.objects.filter(provider=user)
        pending_bookings = Booking.objects.filter(service__in=company_services, status='pending')
        
        return render(request, 'users/dashboard_company.html', {
            'pending_bookings': pending_bookings,
            'user': user,
        })
    else:
        active_bookings = user.client_bookings.filter(date__gte=timezone.now())
        recommended_services = Service.objects.exclude(provider=user)
        notifications = Notification.objects.filter(user=user, is_read=False)  # Notificaciones no leídas

        return render(request, 'users/dashboard_client.html', {
            'active_bookings': active_bookings,
            'recommended_services': recommended_services,
            'notifications': notifications,  # Pasa las notificaciones al template
            'user': user,
        })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})