from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm


def home(request):
    return render(request, 'core/home.html') 

# Vista basada en clase para registro
class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm  # Usa el formulario personalizado
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Asegura que al menos uno de los roles esté seleccionado
        user = form.save(commit=False)
        if not (user.is_company or user.is_client):
            user.is_client = True  # Por defecto, es cliente si no selecciona ninguno
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
        return render(request, 'users/profile_company.html')  # Plantilla para empresas
    return render(request, 'users/profile_client.html')  # Plantilla para clientes

@login_required
def dashboard_view(request):
    user = request.user
    if user.is_company:
        return render(request, 'users/dashboard_company.html')  # Dashboard para empresas
    return render(request, 'users/dashboard_client.html')  # Dashboard para clientes
