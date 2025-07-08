from django.db import transaction
from inventario.models import ReservaInventario
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def registrar_reserva(producto, cantidad, cliente, sucursal, alquiler=None):

    if not all([producto, cantidad, cliente, sucursal]):
        raise ValueError("Faltan datos necesarios para registrar una reserva.")

    with transaction.atomic():
        reserva, creada = ReservaInventario.objects.get_or_create(
            producto=producto,
            cliente=cliente,
            sucursal=sucursal,
            alquiler=alquiler,
            defaults={'cantidad_reservada': cantidad}
        )

        if not creada:
            reserva.cantidad_reservada += cantidad
            reserva.save()

        return reserva
    
@login_required
def listar_reservas(request):
    reservas = ReservaInventario.objects.filter(sucursal=request.user.sucursal).select_related(
        'producto', 'cliente', 'sucursal', 'alquiler'
    ).order_by('-fecha_reserva')

    context = {
        'reservas': reservas,
        'breadcrumb_items': [('Reservas', 'Listado')],
    }
    return render(request, 'listado_reservas.html', context)
