from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventario.forms import DetalleMovimientoInventarioForm, MovimientoInventarioForm
from inventario.models import MovimientoInventario, MovimientoItem
from producto.models import Producto

@login_required
def crear_movimiento(request):
    movimiento = MovimientoInventario.objects.create(
        tipo='entrada',
        sucursal=request.user.sucursal,
        created_by=request.user,
        updated_by=request.user,
    )
    messages.info(request, "Nuevo movimiento creado como borrador.")

    return redirect('editar_movimiento', pk=movimiento.pk)

@login_required
def editar_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk, sucursal=request.user.sucursal)

    form = MovimientoInventarioForm(request.POST or None, instance=movimiento)
    item_form = DetalleMovimientoInventarioForm(request.POST or None)

    if request.method == 'POST' and not request.POST.get('producto'):
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.updated_by = request.user
            movimiento.save()
            messages.success(request, "Movimiento actualizado.")
            return redirect('editar_movimiento', pk=movimiento.pk)

    elif request.method == 'POST' and request.POST.get('producto'):
        producto_id = request.POST.get('producto')
        try:
            producto = Producto.objects.get(id=producto_id, empresa=request.user.empresa)
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado.")
            return redirect('editar_movimiento', pk=movimiento.pk)

        if item_form.is_valid():
            cantidad = item_form.cleaned_data.get('cantidad')
            detalle_existente = movimiento.detalles.filter(producto=producto).first()
            if detalle_existente:
                detalle_existente.cantidad += cantidad
                detalle_existente.save()
            else:
                item = item_form.save(commit=False)
                item.movimiento = movimiento
                item.producto = producto
                item.save()

            messages.success(request, "Producto agregado al movimiento.")
            return redirect('editar_movimiento', pk=movimiento.pk)

    context = {
        'movimiento': movimiento,
        'form': form,
        'item_form': item_form,
        'breadcrumb_items': [
            ('Inventario', '/inventario/stock/'),
            ('Movimientos', '/inventario/movimientos/'),
            (f'Movimiento #{movimiento.id}', None)
        ],
    }
    return render(request, 'editar_movimiento.html', context)


@login_required
def movimiento_list(request):
    movimientos = MovimientoInventario.objects.filter(sucursal=request.user.sucursal).order_by('-fecha')
    context = {
        'movimientos': movimientos,
        'breadcrumb_items': [
            ('Inventario', '/inventario/stock/'),
            ('Movimientos', None)
        ]
    }
    return render(request, 'movimiento_list.html', context)


@login_required
def ver_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk, sucursal=request.user.sucursal)
    context = {
        'movimiento': movimiento,
        'breadcrumb_items': [
            ('Inventario', '/inventario/stock/'),
            ('Movimientos', '/inventario/movimientos/'),
            (f'Movimiento #{movimiento.id}', None)
        ]
    }
    return render(request, 'ver_movimiento.html', context)


@login_required
def confirmar_movimiento(request, pk):
    movimiento = get_object_or_404(MovimientoInventario, pk=pk, sucursal=request.user.sucursal)
    movimiento.updated_by = request.user
    movimiento.save()
    messages.success(request, "Movimiento confirmado correctamente.")

    return redirect('ver_movimiento', pk=movimiento.pk)
