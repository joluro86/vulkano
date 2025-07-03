from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from inventario.models import MovimientoInventario


@login_required
def inventario_list_view(request):
    inventarios = MovimientoInventario.objects.select_related('producto', 'sucursal').order_by('sucursal__nombre', 'producto__nombre')
    return render(request, 'inventario_list_stock.html', {
        'titulo': 'Inventario por Sucursal',
        'inventarios': inventarios,
        'breadcrumb_items': [{'name': 'Inventario', 'url': ''}],
    })
