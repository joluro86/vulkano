from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from alquiler.forms.form_alquiler import AlquilerEditarForm, AlquilerItemForm
from alquiler.models import Alquiler, AlquilerItem
from django.contrib import messages
from django.http import JsonResponse
from inventario.views_stock import consultar_stock_disponible
from producto.models import PrecioProducto, Producto
from cliente.views import obtener_o_crear_cliente_generico
from cliente.models import Cliente
from descuento.models import Descuento
from decimal import Decimal
from django.db.models import F
from alquiler.utils import registrar_evento_alquiler
from django.http import Http404
from django.utils.timezone import now
from django.utils.timezone import localtime
from inventario.views_reserva import registrar_reserva

@login_required
def crear_alquiler(request):
    cliente_generico = obtener_o_crear_cliente_generico(request.user.empresa)

    alquiler = Alquiler.objects.create(
        usuario=request.user,
        cliente=cliente_generico,
        created_by=request.user,
        updated_by=request.user
    )
    messages.info(request, "Nuevo alquiler creado como borrador.")
    return redirect('editar_alquiler', pk=alquiler.pk)

@login_required
def editar_alquiler(request, pk):
    try:
        alquiler = Alquiler.objects.get(pk=pk, usuario__sucursal=request.user.sucursal)
    except Alquiler.DoesNotExist:
        messages.error(request, "El alquiler no existe o no tienes permiso para acceder a él.")
        return redirect('alquiler_list')

    if alquiler.estado in ['anulado', 'liquidado']:
        messages.info(request, f"El alquiler ya fue {alquiler.get_estado_display().lower()} y no puede editarse.")
        return redirect('ver_alquiler', pk=alquiler.pk)

    form = AlquilerEditarForm(request.POST or None, instance=alquiler, sucursal=request.user.sucursal)
    item_form = AlquilerItemForm(request.POST or None, sucursal=request.user.sucursal)

    if request.method == 'POST' and not request.POST.get('producto'):
        if form.is_valid():
            alquiler = form.save(commit=False)
            alquiler.updated_by = request.user
            alquiler.estado = 'reservado'
            alquiler.save()

            registrar_evento_alquiler(
                alquiler,
                tipo='estado',
                descripcion='Alquiler reservado',
                estado_asociado='reservado',
                usuario=request.user
            )

            # Registrar reservas de productos
            for item in alquiler.items.all():
                registrar_reserva(
                    producto=item.producto,
                    cantidad=item.cantidad,
                    cliente=alquiler.cliente,
                    sucursal=request.user.sucursal,
                    alquiler=alquiler
                )

            messages.success(request, "Alquiler actualizado y productos reservados.")
            return redirect('editar_alquiler', pk=alquiler.pk)

    elif request.method == 'POST' and request.POST.get('producto'):
        producto_id = request.POST.get('producto')
        try:
            producto = Producto.objects.get(id=producto_id, empresa=request.user.empresa)
        except Producto.DoesNotExist:
            messages.error(request, "Producto no registrado.")
            return redirect('editar_alquiler', pk=alquiler.pk)

        if item_form.is_valid():
            dias = item_form.cleaned_data.get('dias_a_cobrar')
            cantidad = item_form.cleaned_data.get('cantidad')

            item_existente = alquiler.items.filter(producto=producto).first()
            if item_existente:
                item_existente.dias_a_cobrar = dias or item_existente.dias_a_cobrar
                item_existente.cantidad = cantidad or item_existente.cantidad
                item_existente.save()
            else:
                try:
                    precio = PrecioProducto.objects.get(producto=producto).valor
                except PrecioProducto.DoesNotExist:
                    messages.error(request, "No se encontró un precio registrado para este producto.")
                    return redirect('editar_alquiler', pk=alquiler.pk)

                item = item_form.save(commit=False)
                item.precio_dia = precio
                item.producto = producto
                item.alquiler = alquiler
                item.save()

            if alquiler.estado == 'borrador':
                alquiler.estado = 'en_curso'
                alquiler.save(update_fields=['estado'])
                registrar_evento_alquiler(
                    alquiler,
                    tipo='estado',
                    descripcion='Cambio automático a En curso al agregar producto',
                    estado_asociado='en_curso',
                    usuario=request.user
                )

            alquiler.refresh_from_db()
            form = AlquilerEditarForm(instance=alquiler, sucursal=request.user.sucursal)

    subtotal = Decimal(0)
    descuento_total = Decimal(0)
    iva_total = Decimal(0)
    total_con_descuento = 0

    for item in alquiler.items.select_related('producto'):
        base = item.dias_a_cobrar * item.precio_dia * item.cantidad
        descuento = base * (item.descuento_porcentaje / Decimal('100'))
        subtotal += base
        descuento_total += descuento
        iva = (base - descuento) * (item.producto.iva_porcentaje / Decimal('100'))
        iva_total += iva
        total_con_descuento += (base - descuento)

    alquiler.total = total_con_descuento
    alquiler.save()
    descuentos = Descuento.objects.filter(activo=True, empresa=request.user.empresa)

    context = {
        'alquiler': alquiler,
        'descuentos': descuentos,
        'form': form,
        'item_form': item_form,
        'total': total_con_descuento,
        'subtotal': subtotal,
        'descuento_total': descuento_total,
        'iva_total': iva_total,
        'breadcrumb_items': [('Alquileres', f'Alquiler #{alquiler.id}')],
    }
    return render(request, 'editar_alquiler.html', context)


@login_required
def buscar_productos(request):
    query = request.GET.get('q', '')
    resultados = []
    if len(query) >= 3:
        productos = Producto.objects.filter(
            empresa=request.user.empresa, nombre__icontains=query)[:10]
        resultados = [{'id': p.id, 'nombre': p.nombre} for p in productos]
    return JsonResponse(resultados, safe=False)

@login_required
def eliminar_item_alquiler(request, pk):
    item = AlquilerItem.objects.filter(pk=pk).first()

    if not item:
        messages.error(request, "El producto no existe o ya fue eliminado.")
        return redirect('alquiler_list')

    if item.alquiler.usuario.sucursal != request.user.sucursal:
        messages.error(
            request, "No tienes permiso para eliminar este producto.")
        return redirect('editar_alquiler', pk=item.alquiler.id)

    item.delete()
    messages.success(request, "Producto eliminado del alquiler.")
    return redirect('editar_alquiler', pk=item.alquiler.id)

@login_required
def alquiler_list(request):
    alquileres = Alquiler.objects.filter(
        usuario__sucursal=request.user.sucursal).order_by('-created_at')

    context = {
        'alquileres': alquileres,
        'breadcrumb_items': [('Alquileres', 'Listado')]
    }
    return render(request, 'alquiler_list.html', context)

@login_required
def buscar_clientes(request):
    query = request.GET.get('q', '')
    resultados = []
    if len(query) >= 3:
        clientes = Cliente.objects.filter(
            nombre__icontains=query, empresa=request.user.empresa, estado=True)
        resultados = [{'id': c.id, 'nombre': f"{c.nombre} {c.apellidos}"}
                      for c in clientes]
    return JsonResponse(resultados, safe=False)

@login_required
@require_POST
def aplicar_descuento_alquiler(request, pk):
    alquiler = get_object_or_404(
        Alquiler, pk=pk, usuario__empresa=request.user.empresa)
    descuento_id = request.POST.get('descuento_id')
    descuento = get_object_or_404(
        Descuento, pk=descuento_id, empresa=request.user.empresa, activo=True)

    alquiler.descuento_general = descuento.porcentaje
    alquiler.save()

    for item in alquiler.items.all():
        item.descuento_porcentaje = descuento.porcentaje
        item.save()

    messages.success(
        request, f"Se aplicó el descuento «{descuento.nombre}» correctamente.")
    return redirect('editar_alquiler', pk=pk)

@login_required
def limpiar_descuento(request, pk):
    alquiler = get_object_or_404(
        Alquiler, pk=pk, usuario__empresa=request.user.empresa)

    alquiler.descuento_general = 0
    alquiler.save()

    for item in alquiler.items.all():
        item.descuento_porcentaje = 0
        item.save()

    messages.info(request, f"Se eliminaron correctamente los descuentos.")
    return redirect('editar_alquiler', pk=pk)

@login_required
def anular_alquiler(request, pk):
    try:
        alquiler = get_object_or_404(
            Alquiler,
            pk=pk,
            usuario__empresa=request.user.empresa,
            usuario__sucursal=request.user.sucursal
        )
    except Http404:
        messages.error(request, "El alquiler no existe o no tienes permiso para acceder.")
        return redirect('alquiler_list')

    alquiler.estado = 'anulado'
    alquiler.observaciones = f"Anulado por {request.user.username} - {localtime(now()).strftime('%Y-%m-%d %H:%M:%S')}"
    alquiler.save()
    
    print(alquiler.observaciones)

    messages.success(request, "El alquiler fue anulado correctamente.")
    return redirect('editar_alquiler', pk=pk)
        
@login_required
def ver_alquiler(request, pk):    
    try:
        alquiler = Alquiler.objects.get(pk=pk, usuario__empresa=request.user.empresa)
    except Alquiler.DoesNotExist:
        messages.error(request, f"El alquiler #{pk} no existe o no pertenece a tu empresa.")
        return redirect('alquiler_list')

    # Cálculos necesarios
    subtotal = Decimal(0)
    descuento_total = Decimal(0)
    iva_total = Decimal(0)
    total_con_descuento = Decimal(0)

    for item in alquiler.items.select_related('producto'):
        base = item.dias_a_cobrar * item.precio_dia * item.cantidad
        descuento = base * (item.descuento_porcentaje / Decimal('100'))
        subtotal += base
        descuento_total += descuento
        iva = (base - descuento) * (item.producto.iva_porcentaje / Decimal('100'))
        iva_total += iva
        total_con_descuento += (base - descuento)

    context = {
        'alquiler': alquiler,
        'total': total_con_descuento,
        'subtotal': subtotal,
        'descuento_total': descuento_total,
        'iva_total': iva_total,
        'breadcrumb_items': [('Alquileres', 'Ver')]
    }
    return render(request, 'ver_alquiler.html', context)

@login_required
def liquidar_alquiler(request, pk):
    try:
        alquiler = get_object_or_404(
            Alquiler,
            pk=pk,
            usuario__empresa=request.user.empresa,
            usuario__sucursal=request.user.sucursal
        )
        if alquiler.fecha_fin==None or alquiler.fecha_fin=="" or alquiler.fecha_inicio==None or alquiler.fecha_inicio=="":
            messages.error(request, "Para liquidar el alquiler ingrese fecha de inicio y fecha fin.")
            return redirect('editar_alquiler', pk=pk)
            
    except Http404:
        messages.error(request, "El alquiler no existe o no tienes permiso para acceder.")
        return redirect('alquiler_list')

    alquiler.estado = 'liquidado'
    alquiler.observaciones = f"Liquidado por {request.user.username} - {localtime(now()).strftime('%Y-%m-%d %H:%M:%S')}"
    #alquiler.save()
    
    print(alquiler.observaciones)

    messages.success(request, "El alquiler fue liquidado correctamente.")
    return redirect('ver_alquiler', pk=pk)


@login_required
def reservar_alquiler(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk, usuario__empresa=request.user.empresa)

    if alquiler.estado != 'en_curso':
        messages.warning(request, "Solo se pueden reservar productos de alquileres en estado: En curso.")
        return redirect('editar_alquiler', pk=pk)

    if not alquiler.items.exists():
        messages.warning(request, "No hay productos para reservar en este alquiler.")
        return redirect('editar_alquiler', pk=pk)

    for item in alquiler.items.select_related('producto'):
        cantidad = item.cantidad or 1
        producto = item.producto
        stock_disponible = consultar_stock_disponible(producto, request.user.sucursal)

        if cantidad > stock_disponible:
            messages.error(request, f"Stock insuficiente para {producto.nombre}. "
                                    f"Disponible: {stock_disponible}, requerido: {cantidad}")
            return redirect('editar_alquiler', pk=pk)

        try:
            registrar_reserva(
                producto=producto,
                cantidad=cantidad,
                cliente=alquiler.cliente,
                sucursal=request.user.sucursal,
                alquiler=alquiler
            )
        except Exception as e:
            messages.error(request, f"Error al registrar reserva: {str(e)}")
            return redirect('editar_alquiler', pk=pk)

    alquiler.estado = 'reservado'
    alquiler.save(update_fields=['estado'])
    messages.success(request, "Productos reservados exitosamente.")
    return redirect('editar_alquiler', pk=pk)


from inventario.models import InventarioSucursal, ReservaInventario
from alquiler.utils import registrar_evento_alquiler
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from alquiler.models import Alquiler, AlquilerItem
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def entregar_alquiler(request, pk):
    alquiler = get_object_or_404(
        Alquiler, pk=pk,
        usuario__empresa=request.user.empresa,
        usuario__sucursal=request.user.sucursal
    )

    if alquiler.estado not in ['reservado', 'borrador', 'cotizacion']:
        messages.warning(request, "Este alquiler ya fue entregado o no puede entregarse.")
        return redirect('editar_alquiler', pk=pk)

    try:
        with transaction.atomic():
            for item in alquiler.items.select_related('producto'):
                inventario = InventarioSucursal.objects.filter(
                    producto=item.producto,
                    sucursal=request.user.sucursal
                ).first()

                if not inventario or inventario.stock_actual < item.cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {item.producto.nombre}. "
                        f"Disponible: {inventario.stock_actual if inventario else 0}, Requerido: {item.cantidad}"
                    )

                inventario.stock_actual -= item.cantidad
                inventario.save()

            # Eliminar reservas existentes si las hay
            ReservaInventario.objects.filter(
                alquiler=alquiler,
                entregado=False
            ).delete()

            # Cambiar estado
            alquiler.estado = 'en_curso'
            alquiler.save(update_fields=['estado'])

            registrar_evento_alquiler(
                alquiler,
                tipo='salida',
                descripcion='Productos entregados al cliente.',
                usuario=request.user
            )

            messages.success(request, "Productos entregados correctamente al cliente.")

    except Exception as e:
        messages.error(request, f"Error al entregar productos: {str(e)}")

    return redirect('editar_alquiler', pk=pk)
