from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render
from .models import Reserva  
from django.urls import reverse_lazy
from .forms import ReservaForm, UpdateReservaForm
from cliente.models import Cliente
from producto.models import Producto
from datetime import datetime
from producto.models import PrecioProducto, Producto
from django.contrib import messages 
from reservas.forms.cotizacion import CotizacionForm

class ReservaListView(ListView):
    model = Reserva
    template_name = 'reservas/solicitudes.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        queryset = super().get_queryset()
        for reserva in queryset:
            ultimo_precio = PrecioProducto.objects.filter(producto=reserva.producto).order_by('-id').first()
            reserva.precio = ultimo_precio.valor if ultimo_precio else None
        return queryset


class ReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/crear_reserva.html'
    success_url = reverse_lazy('solicitudes_reserva') 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = self.request.user.empresa  
        return kwargs

    def form_valid(self, form):
        reserva = form.save(commit=False)
        ultimo_precio = PrecioProducto.objects.filter(producto=reserva.producto).order_by('-id').first()
        reserva.precio = ultimo_precio.valor if ultimo_precio else 0
        reserva.save()
        return super().form_valid(form)  

class ReservaUpdateView(UpdateView):
    model = Reserva
    form_class = UpdateReservaForm
    template_name = 'reservas/editar_reserva.html'  
    success_url = reverse_lazy('solicitudes_reserva')

    def form_valid(self, form):
        reserva = form.save(commit=False)
        ultimo_precio = PrecioProducto.objects.filter(producto=reserva.producto).order_by('-id').first()
        if ultimo_precio:
            reserva.precio = ultimo_precio.valor
        else:
            reserva.precio = 0
        reserva.save()
        return super().form_valid(form)  
    
    

def cotizaciones_view(request):
    cotizacion = None
    empresa = request.user.empresa

    if request.method == 'POST':
        form = CotizacionForm(request.POST, empresa=empresa)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            producto = form.cleaned_data['producto']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            dias = (fecha_fin - fecha_inicio).days or 1
            precio = PrecioProducto.objects.filter(producto=producto).order_by('-id').first()
            total = dias * (precio.valor if precio else 0)

            cotizacion = {
                'cliente': cliente.nombre,
                'producto': producto.nombre,
                'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
                'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
                'total': total
            }
        else:
            messages.error(request, "Por favor, corrige los errores del formulario.")
    else:
        form = CotizacionForm(empresa=empresa)

    return render(request, 'reservas/cotizaciones.html', {
        'form': form,
        'cotizacion': cotizacion
    })

def calendario_view(request):
    return render(request, 'reservas/calendario.html')