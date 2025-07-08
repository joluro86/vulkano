from django.db import transaction
from cliente.models import Cliente
from inventario.models import MovimientoInventario, InventarioSucursal, MovimientoItem
from inventario.forms import MovimientoInventarioForm, DetalleMovimientoInventarioForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventario.forms import DetalleMovimientoInventarioForm, MovimientoInventarioForm
from producto.models import Producto, Proveedor
from django.core.paginator import Paginator
from django.db.models import Q


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
    movimiento = get_object_or_404(
        MovimientoInventario, pk=pk, sucursal=request.user.sucursal)

    form = MovimientoInventarioForm(request.POST or None, instance=movimiento)
    item_form = DetalleMovimientoInventarioForm(request.POST or None)

    if request.method == 'POST':
        if request.POST.get('producto'):  # AGREGAR PRODUCTO
            producto_id = request.POST.get('producto')
            try:
                producto = Producto.objects.get(id=producto_id, empresa=request.user.empresa)
            except Producto.DoesNotExist:
                messages.error(request, "Producto no válido.")
                return redirect('editar_movimiento', pk=movimiento.pk)

            if item_form.is_valid():
                cantidad = item_form.cleaned_data.get('cantidad')
                detalle, creado = MovimientoItem.objects.get_or_create(
                    movimiento=movimiento,
                    producto=producto,
                    defaults={'cantidad': cantidad}
                )
                if not creado:
                    detalle.cantidad += cantidad
                    detalle.save()
                messages.success(request, "Producto agregado al movimiento.")
            else:
                messages.error(request, "Error al agregar producto.")
            return redirect('editar_movimiento', pk=movimiento.pk)

        else:  # GUARDAR DATOS GENERALES
            if form.is_valid():
                movimiento = form.save(commit=False)
                movimiento.updated_by = request.user

                tercero_id = request.POST.get('tercero_id')

                if movimiento.tipo == 'entrada':
                    movimiento.cliente = None
                    if tercero_id:
                        try:
                            proveedor = Proveedor.objects.get(id=tercero_id, empresa=request.user.empresa)
                            movimiento.proveedor = proveedor
                        except Proveedor.DoesNotExist:
                            messages.warning(request, "Proveedor no válido.")
                            return redirect('editar_movimiento', pk=movimiento.pk)
                    else:
                        movimiento.proveedor = None

                elif movimiento.tipo == 'salida':
                    movimiento.proveedor = None
                    if tercero_id:
                        try:
                            cliente = Cliente.objects.get(id=tercero_id, empresa=request.user.empresa)
                            movimiento.cliente = cliente
                        except Cliente.DoesNotExist:
                            messages.warning(request, "Cliente no válido.")
                            return redirect('editar_movimiento', pk=movimiento.pk)
                    else:
                        movimiento.cliente = None
                else:
                    movimiento.proveedor = None
                    movimiento.cliente = None

                movimiento.save()
                messages.success(request, "Movimiento actualizado correctamente.")
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
    query = request.GET.get('q', '').strip()
    estado_filtro = request.GET.get('estado', '').strip()

    movimientos_qs = MovimientoInventario.objects.filter(
        sucursal=request.user.sucursal)

    if query:
        movimientos_qs = movimientos_qs.filter(
            Q(id__icontains=query) |
            Q(tipo__icontains=query)
        )

    if estado_filtro:
        movimientos_qs = movimientos_qs.filter(estado=estado_filtro)

    movimientos_qs = movimientos_qs.order_by('-fecha')

    paginator = Paginator(movimientos_qs, 10)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)

    total_movimientos = f"Total movimientos: {movimientos_qs.count()}"

    context = {
        'movimientos': movimientos,
        'query': query,
        'estado_filtro': estado_filtro,
        'total_movimientos': total_movimientos,
        'breadcrumb_items': [
            ('Inventario', '/inventario/stock/'),
            ('Movimientos', None)
        ]
    }
    return render(request, 'movimiento_list.html', context)


@login_required
def ver_movimiento(request, pk):
    movimiento = get_object_or_404(
        MovimientoInventario, pk=pk, sucursal=request.user.sucursal)
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
def eliminar_item_movimiento(request, pk):
    item = get_object_or_404(MovimientoItem, pk=pk)
    movimiento = item.movimiento

    # Verificamos que el usuario tenga acceso a la sucursal
    if movimiento.sucursal != request.user.sucursal:
        messages.error(
            request, "No tienes permiso para eliminar este producto.")
        return redirect('editar_movimiento', pk=movimiento.pk)

    if request.method == 'POST':
        item.delete()
        messages.success(
            request, f"Producto eliminado del movimiento #{movimiento.id}.")

    return redirect('editar_movimiento', pk=movimiento.pk)


@login_required
def confirmar_movimiento(request, pk):
    movimiento = get_object_or_404(
        MovimientoInventario, pk=pk, sucursal=request.user.sucursal)

    if movimiento.estado != 'borrador':
        messages.warning(
            request, "Este movimiento ya ha sido confirmado o anulado.")
        return redirect('editar_movimiento', pk=pk)

    if not movimiento.items.exists():
        messages.error(
            request, "No puedes confirmar un movimiento sin productos.")
        return redirect('editar_movimiento', pk=pk)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Validación previa para salidas
                if movimiento.tipo == 'salida':
                    for item in movimiento.items.all():
                        inventario = InventarioSucursal.objects.filter(
                            producto=item.producto,
                            sucursal=movimiento.sucursal
                        ).first()
                        stock_disponible = inventario.stock_actual if inventario else 0
                        if item.cantidad > stock_disponible:
                            messages.error(
                                request,
                                f"No hay suficiente stock de {item.producto.nombre}. Disponible: {stock_disponible}, requerido: {item.cantidad}"
                            )
                            return redirect('editar_movimiento', pk=pk)

                # Aplicar movimiento
                for item in movimiento.items.all():
                    inventario, _ = InventarioSucursal.objects.get_or_create(
                        producto=item.producto,
                        sucursal=movimiento.sucursal,
                        defaults={'stock_actual': 0}
                    )

                    if movimiento.tipo == 'entrada':
                        inventario.stock_actual += item.cantidad
                    elif movimiento.tipo == 'salida':
                        inventario.stock_actual -= item.cantidad
                    else:
                        messages.warning(
                            request, "Este tipo de movimiento aún no afecta inventario.")
                        return redirect('editar_movimiento', pk=pk)

                    inventario.save()

                movimiento.estado = 'confirmado'
                movimiento.save()

                messages.success(
                    request, "Movimiento confirmado y stock actualizado correctamente.")
        except Exception as e:
            messages.error(
                request, f"Ocurrió un error al confirmar el movimiento: {str(e)}")

    return redirect('editar_movimiento', pk=pk)
