from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from inventario.models import InventarioSucursal
from empresa.models import Sucursal
from django.core.paginator import Paginator
from django.db.models import Q
from inventario.models import InventarioSucursal, ReservaInventario
from django.db.models import Sum

from inventario.models import InventarioSucursal, ReservaInventario
from django.db.models import Sum, F

from alquiler.models import AlquilerItem

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
        reservado = ReservaInventario.objects.filter(
            producto=inv.producto,
            sucursal=inv.sucursal,
            entregado=False
        )
        
            
        reservado = ReservaInventario.objects.filter(
            producto=inv.producto,
            sucursal=inv.sucursal,
            entregado=False
        ).aggregate(total=Sum('cantidad_reservada'))['total'] or 0

        entregado = AlquilerItem.objects.filter(
            producto=inv.producto,
            alquiler__estado='en_curso',
            alquiler__usuario__sucursal=inv.sucursal
        ).aggregate(total=Sum('cantidad'))['total'] or 0

        inventarios_list.append({
            'item': inv,
            'reservado': reservado,
            'entregado': entregado,
            'stock_disponible': inv.stock_actual - reservado,  # entregado ya fue descontado al momento de la entrega
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
            ("Inventario", reverse('inventario_list_stock')),  # o la vista anterior si existe
            ("Stock", None)
        ],
    })

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
