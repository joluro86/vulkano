from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from inventario.models import InventarioSucursal


@login_required
def inventario_list_view(request):
    inventarios = InventarioSucursal.objects.select_related('producto', 'sucursal').order_by('sucursal__nombre', 'producto__nombre')
    print(inventarios)
    return render(request, 'inventario_list_stock.html', {
        'titulo': 'Inventario por Sucursal',
        'inventarios': inventarios,
        'breadcrumb_items': [{'Stock': 'Inventario', 'url': ''}],
    })
