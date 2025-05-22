from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PrecioProducto
from producto.forms.forms_precio_producto import PrecioProductoForm
from producto.models import Producto 
from django.db.models import Count

@login_required
def precio_producto_list(request):
    precios = PrecioProducto.objects.filter(
        producto__empresa=request.user.empresa).order_by('producto__nombre')
    return render(request, 'precio_producto_list.html', {
        'precios': precios,
        'breadcrumb_items': [('Gestión de productos', '#'), ('Precios', 'Listado')],
    })


@login_required
def precio_producto_create(request):
    form = PrecioProductoForm(request.POST or None)
    form.fields['producto'].queryset = Producto.objects.filter(empresa=request.user.empresa).annotate(
        num_precios=Count('precios')
    ).filter(
        num_precios=0
    )

    if request.method == 'POST' and form.is_valid():
        precio = form.save(commit=False)
        if precio.producto.empresa != request.user.empresa:
            messages.error(
                request, "No puedes asignar un producto que no pertenece a tu empresa.")
        else:
            precio.save()
            messages.success(request, "Precio creado exitosamente.")
            return redirect('precio_producto_list')

    return render(request, 'precio_producto_form.html', {
        'form': form,
        'titulo': 'Crear precio',
        'boton_texto': 'Guardar',
        'breadcrumb_items': [('Gestión de productos', '#'), ('Precios', 'Crear')],
    })


@login_required
def precio_producto_edit(request, pk):
    precio = get_object_or_404(
        PrecioProducto, pk=pk, producto__empresa=request.user.empresa)
    form = PrecioProductoForm(request.POST or None, instance=precio)
    form.fields['producto'].queryset = Producto.objects.filter(
        empresa=request.user.empresa)

    if request.method == 'POST' and form.is_valid():
        precio = form.save(commit=False)
        if precio.producto.empresa != request.user.empresa:
            messages.error(
                request, "No puedes modificar con un producto que no pertenece a tu empresa.")
        else:
            precio.save()
            messages.success(request, "Precio actualizado correctamente.")
            return redirect('precio_producto_list')

    return render(request, 'precio_producto_form.html', {
        'form': form,
        'titulo': 'Editar precio',
        'boton_texto': 'Actualizar',
        'breadcrumb_items': [('Gestión de productos', '#'), ('Precios', 'Editar')],
    })


@login_required
def precio_producto_delete(request, pk):
    precio = get_object_or_404(
        PrecioProducto, pk=pk, producto__empresa=request.user.empresa)
    if request.method == 'POST':
        precio.delete()
        messages.success(request, "Precio eliminado.")
        return redirect('precio_producto_list')
    return render(request, 'precio_producto_confirm_delete.html', {
        'precio': precio,
        'breadcrumb_items': [('Gestión de productos', '#'), ('Precios', 'Eliminar')],
    })
