from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from alquiler.forms.form_alquiler import AlquilerEditarForm, AlquilerItemForm
from alquiler.models import Alquiler, AlquilerItem
from django.contrib import messages

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

    # Guardar fechas/observación
    if request.method == 'POST' and 'producto' not in request.POST:
        if form.is_valid():
            alquiler = form.save(commit=False)
            alquiler.updated_by = request.user
            alquiler.save()
            return redirect('editar_alquiler', pk=alquiler.pk)

    # Agregar o actualizar producto
    elif request.method == 'POST' and 'producto' in request.POST:
        if item_form.is_valid():
            producto = item_form.cleaned_data['producto']
            dias = item_form.cleaned_data['dias_a_cobrar']
            precio = item_form.cleaned_data['precio_dia']

            item_existente = alquiler.items.filter(producto=producto).first()

            if item_existente:
                item_existente.dias_a_cobrar = dias
                item_existente.precio_dia = precio
                item_existente.save()
            else:
                item = item_form.save(commit=False)
                item.alquiler = alquiler
                item.save()

            # 🔁 Refrescar datos del alquiler y el form principal
            alquiler.refresh_from_db()
            form = AlquilerEditarForm(instance=alquiler)

    context = {
        'alquiler': alquiler,
        'form': form,
        'item_form': item_form,
        'breadcrumb_items': [('Alquileres', f'Alquiler #{alquiler.id}')]
    }
    return render(request, 'editar_alquiler.html', context)


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
