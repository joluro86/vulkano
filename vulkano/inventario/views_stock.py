from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventario.models import InventarioSucursal
from empresa.models import Sucursal
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def inventario_list_stock(request):
    query = request.GET.get('q', '').strip()
    sucursal_id = request.GET.get('sucursal_id', '').strip()

    inventarios_qs = InventarioSucursal.objects.select_related('producto', 'sucursal')

    # Filtrar por empresa del usuario (si corresponde)
    if hasattr(request.user, 'empresa'):
        inventarios_qs = inventarios_qs.filter(producto__empresa=request.user.empresa)

    # Filtro por nombre de producto
    if query:
        inventarios_qs = inventarios_qs.filter(producto__nombre__icontains=query)

    # Filtro por sucursal
    if sucursal_id:
        inventarios_qs = inventarios_qs.filter(sucursal_id=sucursal_id)

    inventarios_qs = inventarios_qs.order_by('producto__nombre')

    paginator = Paginator(inventarios_qs, 10)
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
        'breadcrumb_items': [('Inventario', 'Stock por sucursal')],
    })

from inventario.models import InventarioSucursal, ReservaInventario
from django.db.models import Sum

def consultar_stock_disponible(producto, sucursal):
    """
    Retorna el stock disponible real de un producto en una sucursal,
    descontando las reservas no entregadas.
    """
    inventario = InventarioSucursal.objects.filter(producto=producto, sucursal=sucursal).first()

    if not inventario:
        return 0

    reservados = ReservaInventario.objects.filter(
        producto=producto,
        sucursal=sucursal,
        entregado=False
    ).aggregate(total=Sum('cantidad_reservada'))['total'] or 0

    return inventario.stock_actual - reservados
