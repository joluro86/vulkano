from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from alquiler.forms.form_alquiler import AlquilerEditarForm, AlquilerItemForm
from alquiler.models import Alquiler, AlquilerItem
from django.contrib import messages
from django.http import JsonResponse
from producto.models import Producto
from django.db.models import Sum

@login_required
def crear_alquiler(request):
    alquiler = Alquiler.objects.create(
        usuario=request.user,
        created_by=request.user,
        updated_by=request.user
    )
    return redirect('editar_alquiler', pk=alquiler.pk)

@login_required
def editar_alquiler(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk, usuario__sucursal=request.user.sucursal)

    # Formularios iniciales
    form = AlquilerEditarForm(request.POST or None, instance=alquiler)
    item_form = AlquilerItemForm(request.POST or None, sucursal=request.user.sucursal)

    # Guardar fechas/observaciones
    if request.method == 'POST' and not request.POST.get('producto'):
        if form.is_valid():
            alquiler = form.save(commit=False)
            alquiler.updated_by = request.user
            alquiler.save()
            messages.success(request, "Datos del alquiler actualizados.")
            return redirect('editar_alquiler', pk=alquiler.pk)

    # Agregar producto
    elif request.method == 'POST' and request.POST.get('producto'):
        producto_id = request.POST.get('producto')
        try:
            producto = Producto.objects.get(id=producto_id, sucursal=request.user.sucursal)
        except Producto.DoesNotExist:
            messages.error(request, "Producto no válido.")
            return redirect('editar_alquiler', pk=alquiler.pk)

        if item_form.is_valid():
            dias = item_form.cleaned_data.get('dias_a_cobrar')
            precio = item_form.cleaned_data.get('precio_dia')

            item_existente = alquiler.items.filter(producto=producto).first()
            if item_existente:
                item_existente.dias_a_cobrar = dias or item_existente.dias_a_cobrar
                item_existente.precio_dia = precio or item_existente.precio_dia
                item_existente.save()
            else:
                item = item_form.save(commit=False)
                item.producto = producto
                item.alquiler = alquiler
                item.save()

            alquiler.refresh_from_db()
            form = AlquilerEditarForm(instance=alquiler)
    total = alquiler.items.aggregate(total=Sum('valor_item'))['total'] or 0
    context = {
        'alquiler': alquiler,
        'form': form,
        'item_form': item_form,
        'breadcrumb_items': [('Alquileres', f'Alquiler #{alquiler.id}')],
        'total': total
    }
    return render(request, 'editar_alquiler.html', context)

@login_required
def buscar_productos(request):
    query = request.GET.get('q', '')
    resultados = []
    if len(query) >= 3:
        productos = Producto.objects.filter(nombre__icontains=query)[:10]
        resultados = [{'id': p.id, 'nombre': p.nombre} for p in productos]
    return JsonResponse(resultados, safe=False)

@login_required
def eliminar_item_alquiler(request, pk):
    item = AlquilerItem.objects.filter(pk=pk).first()

    if not item:
        messages.error(request, "El producto no existe o ya fue eliminado.")
        return redirect('alquiler_list')

    if item.alquiler.usuario.sucursal != request.user.sucursal:
        messages.error(request, "No tienes permiso para eliminar este producto.")
        return redirect('editar_alquiler', pk=item.alquiler.id)

    item.delete()
    return redirect('editar_alquiler', pk=item.alquiler.id)
