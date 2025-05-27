from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from alquiler.forms.form_alquiler import AlquilerEditarForm, AlquilerItemForm
from alquiler.models import Alquiler, AlquilerItem
from django.contrib import messages
from django.http import JsonResponse
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
            alquiler.estado = 'en_curso'
            alquiler.save()

            registrar_evento_alquiler(
                alquiler,
                tipo='estado',
                descripcion='Se crea el alquiler y pasa a estado en curso',
                estado_asociado='en_curso',
                usuario=request.user
            )

            messages.success(request, "Datos del alquiler actualizados.")
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
    except Http404:
        messages.error(request, "El alquiler no existe o no tienes permiso para acceder.")
        return redirect('alquiler_list')

    alquiler.estado = 'liquidado'
    alquiler.observaciones = f"Liquidado por {request.user.username} - {localtime(now()).strftime('%Y-%m-%d %H:%M:%S')}"
    alquiler.save()
    
    print(alquiler.observaciones)

    messages.success(request, "El alquiler fue liquidado correctamente.")
    return redirect('ver_alquiler', pk=pk)