from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render
from .models import Reserva  
from django.urls import reverse_lazy
from .forms import ReservaForm, UpdateReservaForm
from cliente.models import Cliente
from producto.models import Producto
from datetime import datetime

class ReservaListView(ListView):
    model = Reserva
    template_name = 'reservas/solicitudes.html'
    context_object_name = 'reservas'


class ReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/crear_reserva.html'
    success_url = reverse_lazy('solicitudes_reserva')    

class ReservaUpdateView(UpdateView):
    model = Reserva
    form_class = UpdateReservaForm
    template_name = 'reservas/editar_reserva.html'  # El template para el formulario de edición
    success_url = reverse_lazy('solicitudes_reserva')  # URL a la que redirige después de guardar

def cotizaciones_view(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    cotizacion = None

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        producto_id = request.POST.get('producto')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            producto = Producto.objects.get(id=producto_id)
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            dias = (fecha_fin_dt - fecha_inicio_dt).days + 1
            total = dias * producto.precio  # Suponiendo que tiene campo 'precio'

            cotizacion = {
                'cliente': cliente.nombre,
                'producto': producto.nombre,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'total': total,
            }

        except Exception as e:
            print(f"Error al calcular cotización: {e}")

    return render(request, 'reservas/cotizaciones.html', {
        'clientes': clientes,
        'productos': productos,
        'cotizacion': cotizacion
    })


def calendario_view(request):
    return render(request, 'reservas/calendario.html')