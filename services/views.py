# services/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Service
from .forms import ServiceForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def service_list(request):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Si es empresa, muestra solo los servicios que ha publicado
        if request.user.is_company:
            services = Service.objects.filter(provider=request.user)
        # Si es cliente, muestra todos los servicios
        else:
            services = Service.objects.all()
    else:
        # Si no está autenticado, muestra todos los servicios
        services = Service.objects.all()
    
    return render(request, 'services/service_list.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user  
            service.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})

def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_detail', pk=pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'service': service})