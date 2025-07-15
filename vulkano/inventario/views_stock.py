from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from inventario.models import InventarioSucursal, MovimientoInventario, MovimientoItem, ReservaInventario
from empresa.models import Sucursal
from alquiler.models import Alquiler, AlquilerItem


# Función reutilizable para calcular stock disponible
def calcular_stock_disponible(producto, sucursal):
    reservado = ReservaInventario.objects.filter(
        producto=producto,
        sucursal=sucursal,
        entregado=False
    ).aggregate(total=Sum('cantidad_reservada'))['total'] or 0

    entregado = AlquilerItem.objects.filter(
        producto=producto,
        alquiler__usuario__sucursal=sucursal,
        alquiler__estado='despachado'
    ).aggregate(total=Sum('cantidad'))['total'] or 0

    return reservado, entregado


# Vista para actualizar el stock_actual de cada producto
@login_required
def actualizar_stock_disponible(request):
    sucursal = request.user.sucursal
    inventarios = InventarioSucursal.objects.filter(sucursal=sucursal)

    for inv in inventarios:
        reservado, entregado = calcular_stock_disponible(inv.producto, sucursal)
        inv.stock_actual = max(inv.total_historico - reservado - entregado, 0)
        inv.save(update_fields=['stock_actual'])

    messages.success(request, "Stock actualizado correctamente.")
    return redirect('inventario_list_stock')


# Vista principal del listado de inventario con paginación y filtros
@login_required
def inventario_list_stock(request):
    query = request.GET.get('q', '').strip()
    sucursal_id = request.GET.get('sucursal_id', '').strip()

    inventarios_qs = InventarioSucursal.objects.select_related('producto', 'sucursal')

    if hasattr(request.user, 'empresa'):
        inventarios_qs = inventarios_qs.filter(producto__empresa=request.user.empresa)

    if query:
        inventarios_qs = inventarios_qs.filter(producto__nombre__icontains=query)

    if sucursal_id:
        inventarios_qs = inventarios_qs.filter(sucursal_id=sucursal_id)

    inventarios_qs = inventarios_qs.order_by('producto__nombre')

    inventarios_list = []
    for inv in inventarios_qs:
        reservado, entregado = calcular_stock_disponible(inv.producto, inv.sucursal)
        inventarios_list.append({
            'item': inv,
            'reservado': reservado,
            'entregado': entregado,
            'stock_disponible': inv.stock_actual - reservado,
        })

    paginator = Paginator(inventarios_list, 10)
    page_number = request.GET.get('page')
    inventarios = paginator.get_page(page_number)

    total_inventarios = f"Total productos en inventario: {inventarios_qs.count()}"
    sucursales = Sucursal.objects.filter(empresa=request.user.empresa)

    return render(request, 'inventario_list_stock.html', {
        'inventarios': inventarios,
        'query': query,
        'sucursal_filtro': sucursal_id,
        'total_inventarios': total_inventarios,
        'sucursales': sucursales,
        'breadcrumb_items': [
            ("Inventario", reverse('inventario_list_stock')),
            ("Stock", None)
        ],
    })


# Consulta rápida para usar desde otras vistas (sin entregado)
def consultar_stock_disponible(producto, sucursal):
    inventario = InventarioSucursal.objects.filter(producto=producto, sucursal=sucursal).first()
    if not inventario:
        return 0
    reservado, _ = calcular_stock_disponible(producto, sucursal)
    return inventario.stock_actual - reservado

def limpiar_inventario(request):
    InventarioSucursal.objects.all().delete()
    MovimientoInventario.objects.all().delete()
    MovimientoItem.objects.all().delete()
    ReservaInventario.objects.all().delete()
    AlquilerItem.objects.all().delete()
    Alquiler.objects.all().delete()
    return redirect('inventario_list_stock')

    
    