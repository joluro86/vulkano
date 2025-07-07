from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PrecioProducto
from producto.forms.forms_precio_producto import PrecioProductoForm
from producto.models import Producto 
from django.db.models import Count

from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def precio_producto_list(request):
    query = request.GET.get('q', '').strip()

    precios_qs = PrecioProducto.objects.filter(
        producto__empresa=request.user.empresa
    )

    if query:
        precios_qs = precios_qs.filter(producto__nombre__icontains=query)

    precios_qs = precios_qs.order_by('producto__nombre')

    paginator = Paginator(precios_qs, 10)
    page_number = request.GET.get('page')
    precios = paginator.get_page(page_number)

    total_precios = f"Total precios registrados: {precios_qs.count()}"

    return render(request, 'precio_producto_list.html', {
        'precios': precios,
        'query': query,
        'total_precios': total_precios,
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
