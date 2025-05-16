from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cliente.models import Cliente
from cliente.forms import ClienteForm

@login_required
def cliente_list(request):
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'cliente_list.html', {
        'clientes': clientes,
        'breadcrumb_items': [('Clientes', 'Listado')],
    })

@login_required
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cliente = form.save(commit=False)
        cliente.empresa = request.user.empresa
        cliente.save()
        messages.success(request, "Cliente creado exitosamente.")
        return redirect('cliente_list')
    return render(request, 'cliente_form.html', {
        'form': form,
        'titulo': 'Crear cliente',
        'boton_texto': 'Guardar cliente',
        'breadcrumb_items': [('Clientes', 'Crear')],
    })


@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Cliente actualizado exitosamente.")
        return redirect('cliente_list')
    return render(request, 'cliente_form.html', {
        'form': form,
        'titulo': 'Editar cliente',
        'boton_texto': 'Actualizar cliente',
        'breadcrumb_items': [('Clientes', f'Editar: {cliente.nombre}')],
    })

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, "Cliente eliminado.")
        return redirect('cliente_list')
    return render(request, 'cliente_confirm_delete.html', {
        'cliente': cliente,
        'breadcrumb_items': [('Clientes', f'Eliminar: {cliente.nombre}')],
    })
