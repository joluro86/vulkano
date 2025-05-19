from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from descuento.models import Descuento
from descuento.form import DescuentoForm

@login_required
def descuento_list(request):
    descuentos = Descuento.objects.filter(empresa=request.user.empresa)
    return render(request, 'descuento_list.html', {
        'descuentos': descuentos,
        'breadcrumb_items': [('Alquileres', 'Descuentos')],
    })


@login_required
def descuento_create(request):
    form = DescuentoForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        descuento = form.save(commit=False)
        descuento.empresa = request.user.empresa
        descuento.creado_por = request.user.get_full_name()
        descuento.save()
        messages.success(request, "Descuento creado exitosamente.")
        return redirect('descuento_list')  # asegúrate que esta URL exista
    
    context = {
        'form': form,
        'titulo': 'Crear descuento',
        'boton_texto': 'Guardar descuento',
        'breadcrumb_items': [('Descuentos', 'Crear')]
    }
    return render(request, 'descuento_form.html', context)

@login_required
def descuento_edit(request, pk):
    descuento = get_object_or_404(Descuento, pk=pk, empresa=request.user.empresa)
    form = DescuentoForm(request.POST or None, instance=descuento)

    if request.method == 'POST' and form.is_valid():
        descuento = form.save(commit=False)
        descuento.modificado_por = request.user.get_full_name()
        descuento.save()
        messages.success(request, "Descuento actualizado correctamente.")
        return redirect('descuento_list')

    context = {
        'form': form,
        'titulo': 'Editar descuento',
        'boton_texto': 'Actualizar',
        'breadcrumb_items': [('Descuentos', 'Editar')]
    }
    return render(request, 'descuento_form.html', context)

@login_required
def descuento_delete(request, pk):
    descuento = get_object_or_404(Descuento, pk=pk)
    if request.method == 'POST':
        descuento.delete()
        messages.success(request, "Descuento eliminado.")
        return redirect('descuento_list')
    return render(request, 'descuento_confirm_delete.html', {
        'descuento': descuento,
        'breadcrumb_items': [('Alquileres', 'Eliminar descuento')],
    })
