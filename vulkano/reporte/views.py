from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from alquiler.models import AbonoAlquiler, LiquidacionAlquiler

@login_required
def informe_ingresos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    abonos = AbonoAlquiler.objects.all()
    liquidaciones = LiquidacionAlquiler.objects.all()

    if fecha_inicio and fecha_fin:
        abonos = abonos.filter(fecha__range=[fecha_inicio, fecha_fin])
        liquidaciones = liquidaciones.filter(fecha__range=[fecha_inicio, fecha_fin])

    total_abonos = abonos.aggregate(total=Sum('valor'))['total'] or 0
    total_liquidado = liquidaciones.aggregate(total=Sum('total_liquidado'))['total'] or 0

    return render(request, 'informe_ingresos.html', {
        'abonos': abonos,
        'liquidaciones': liquidaciones,
        'total_abonos': total_abonos,
        'total_liquidado': total_liquidado,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'breadcrumb_items': [
            ("Reportes", None),
            ("Informe de ingresos", None)
        ]
    })

# reporte/views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from alquiler.models import Alquiler
from cliente.models import Cliente

@login_required
def resumen_alquileres(request):
    cliente_id = request.GET.get('cliente')
    estado = request.GET.get('estado')
    fecha_inicio = request.GET.get('desde')
    fecha_fin = request.GET.get('hasta')

    alquileres = Alquiler.objects.select_related('cliente').filter(
        usuario__empresa=request.user.empresa
    )

    if cliente_id:
        alquileres = alquileres.filter(cliente_id=cliente_id)

    if estado:
        alquileres = alquileres.filter(estado=estado)

    if fecha_inicio:
        alquileres = alquileres.filter(fecha_inicio__gte=fecha_inicio)

    if fecha_fin:
        alquileres = alquileres.filter(fecha_fin__lte=fecha_fin)

    clientes = Cliente.objects.filter(empresa=request.user.empresa)

    context = {
        'alquileres': alquileres,
        'clientes': clientes,
        'estados': Alquiler.ESTADOS_ALQUILER,
    }
    return render(request, 'resumen_alquileres.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from alquiler.models import Alquiler
from django.db.models import Q
from django.urls import reverse

@login_required
def informe_economico(request):
    alquileres = Alquiler.objects.select_related('cliente').filter(usuario__empresa=request.user.empresa)

    cliente = request.GET.get('cliente', '').strip()
    estado = request.GET.get('estado', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()

    if cliente:
        alquileres = alquileres.filter(cliente__nombre__icontains=cliente)

    if estado:
        alquileres = alquileres.filter(estado=estado)

    if fecha_inicio:
        alquileres = alquileres.filter(fecha_inicio__gte=fecha_inicio)

    if fecha_fin:
        alquileres = alquileres.filter(fecha_fin__lte=fecha_fin)

    return render(request, 'resumen_alquileres.html', {
        'alquileres': alquileres.order_by('-fecha_inicio'),
        'breadcrumb_items': [("Reportes", reverse('informe_economico_alquileres'))],
        'estados': Alquiler.ESTADOS_ALQUILER,
    })
