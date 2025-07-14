from django.contrib.auth.decorators import login_required
from alquiler.forms.form_alquiler import AbonoAlquilerForm, AlquilerEditarForm, AlquilerItemForm
from alquiler.models import AbonoAlquiler, Alquiler, AlquilerItem, LiquidacionAlquiler
from django.contrib import messages
from django.http import JsonResponse
from inventario.views_stock import consultar_stock_disponible
from producto.models import PrecioProducto, Producto
from cliente.views import obtener_o_crear_cliente_generico
from cliente.models import Cliente
from descuento.models import Descuento
from decimal import Decimal
from alquiler.utils import registrar_evento_alquiler
from django.http import Http404
from django.utils.timezone import now, localtime
from inventario.views_reserva import registrar_reserva
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from alquiler.models import Alquiler
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from inventario.models import InventarioSucursal, ReservaInventario
from alquiler.utils import registrar_evento_alquiler
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from alquiler.models import Alquiler, AlquilerItem
from django.db.models import Sum
from alquiler.forms.form_alquiler import AbonoAlquilerForm

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

    abonos_total = alquiler.total_abonado 
    saldo_pendiente = alquiler.saldo_pendiente
    
    context = {
        'alquiler': alquiler,
        'descuentos': descuentos,
        'form': form,
        'item_form': item_form,
        'total': total_con_descuento,
        'subtotal': subtotal,
        'descuento_total': descuento_total,
        'iva_total': iva_total,
        'abonos_total': abonos_total,
        'saldo_pendiente': saldo_pendiente,
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
    estado = request.GET.get('estado', '')
    qs = Alquiler.objects.filter(usuario__sucursal=request.user.sucursal)

    if estado:
        qs = qs.filter(estado=estado)

    qs = qs.order_by('-created_at')
    paginator = Paginator(qs, 10)  # 10 alquileres por página
    page_number = request.GET.get('page')
    alquileres = paginator.get_page(page_number)

    return render(request, 'alquiler_list.html', {
        'alquileres': alquileres,
        'estado_filtro': estado,
        'breadcrumb_items': [('Alquileres', None)]
    })

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
    except Http404:
        messages.error(request, "El alquiler no existe o no tienes permiso para acceder.")
        return redirect('alquiler_list')

    if not alquiler.fecha_inicio or not alquiler.fecha_fin:
        messages.error(request, "Para liquidar el alquiler, debes ingresar fecha de inicio y fecha fin.")
        return redirect('editar_alquiler', pk=pk)

    if alquiler.estado == 'liquidado':
        messages.info(request, "El alquiler ya fue liquidado.")
        return redirect('editar_alquiler', pk=pk)

    abonos_total = alquiler.abonos.aggregate(total=Sum('valor'))['total'] or 0
    saldo_pendiente = max(alquiler.total - abonos_total, 0)

    if saldo_pendiente > 0:
        messages.warning(request, f"No se puede liquidar: hay un saldo pendiente de ${saldo_pendiente:,.0f}")
        return redirect('editar_alquiler', pk=pk)

    # Guardar liquidación
    LiquidacionAlquiler.objects.create(
        alquiler=alquiler,
        total_liquidado=abonos_total,
        observaciones=f"Liquidado automáticamente por {request.user.get_full_name()}",
        liquidado_por=request.user
    )

    alquiler.estado = 'liquidado'
    alquiler.observaciones += f"\nLiquidado por {request.user.username} - {localtime(now()).strftime('%Y-%m-%d %H:%M:%S')}"
    alquiler.save(update_fields=['estado', 'observaciones'])

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

@login_required
def abonar_alquiler(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk, usuario__empresa=request.user.empresa)

    if alquiler.estado == 'liquidado':
        messages.warning(request, "Este alquiler ya fue liquidado. No se puede abonar.")
        return redirect('editar_alquiler', pk=pk)

    form = AbonoAlquilerForm(request.POST or None)

    # Calcular saldo pendiente
    total_abonado = alquiler.abonos.aggregate(total=Sum('valor'))['total'] or 0
    saldo_pendiente = alquiler.total_con_descuento - total_abonado

    if request.method == 'POST' and form.is_valid():
        abono = form.save(commit=False)

        if abono.valor > saldo_pendiente:
            messages.error(request, f"El abono no puede ser mayor al saldo pendiente (${saldo_pendiente:,.0f}).")
        else:
            abono.alquiler = alquiler
            abono.registrado_por = request.user
            abono.save()
            messages.success(request, f"Abono de ${abono.valor:,.0f} registrado correctamente.")
            return redirect('editar_alquiler', pk=pk)

    return render(request, 'abonar_alquiler.html', {
        'form': form,
        'alquiler': alquiler,
        'saldo_pendiente': saldo_pendiente,
        'breadcrumb_items': [('Alquileres', 'Abonar')],
    })
    
def ver_abonos_alquiler(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk, usuario__empresa=request.user.empresa)
    abonos = alquiler.abonos.all()
    total_abonado = abonos.aggregate(total=Sum('valor'))['total'] or 0
    total_pagar = alquiler.total_con_descuento
    saldo_pendiente = total_pagar - total_abonado

    return render(request, 'ver_abonos.html', {
        'alquiler': alquiler,
        'abonos': abonos,
        'total_abonado': total_abonado,
        'total_pagar': total_pagar,
        'saldo_pendiente': saldo_pendiente,
        'breadcrumb_items': [('Alquileres', f'Alquiler #{alquiler.id}')],
    })

@login_required
def eliminar_abono(request, pk):
    abono = get_object_or_404(AbonoAlquiler, pk=pk)

    if request.method == 'POST':
        alquiler_id = abono.alquiler.id
        abono.delete()
        messages.success(request, "Abono eliminado correctamente.")
        return redirect('ver_abonos_alquiler', pk=alquiler_id)

    messages.error(request, "Método no permitido.")
    return redirect('ver_abonos_alquiler', pk=abono.alquiler.id)