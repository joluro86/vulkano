from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cliente.models import Cliente
from cliente.forms import ClienteForm
from django.db.models import ProtectedError
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def cliente_list(request):
    query = request.GET.get('q', '').strip()
    clientes_qs = Cliente.objects.filter(empresa=request.user.empresa)
    total_clientes= len(Cliente.objects.filter(empresa=request.user.empresa))
    if query:
        clientes_qs = clientes_qs.filter(
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(documento__icontains=query) |
            Q(correo__icontains=query)
        )

    clientes_qs = clientes_qs.order_by('nombre')
    paginator = Paginator(clientes_qs, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)
    
    total_clientes= "Total clientes: " + str(total_clientes)

    return render(request, 'cliente_list.html', {
        'clientes': clientes,
        'total_clientes': total_clientes,
        'query': query,
        'estado_filtro': 'todos',
        'breadcrumb_items': [('Clientes', 'Listado')],
    })

@login_required
def cliente_list_por_estado(request, estado):
    
    if estado=="activos":
        clientes= Cliente.objects.filter(empresa=request.user.empresa, estado=True)
    else:
        clientes= Cliente.objects.filter(empresa=request.user.empresa, estado=False)
            
    total_clientes= len(clientes)

    clientes = clientes.order_by('nombre')
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)
    
    total_clientes= "Total clientes: " + str(total_clientes)

    return render(request, 'cliente_list.html', {
        'clientes': clientes,
        'total_clientes': total_clientes,
        'estado_filtro': estado,
        'breadcrumb_items': [('Clientes', 'Listado')],
    })


@login_required
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if Cliente.objects.filter(documento=form.cleaned_data.get("documento"), empresa=request.user.empresa).exists():
            messages.error(request, "Ya existe un cliente con ese documento en esta empresa.")

        else:
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
    
    try:
        if request.method == 'POST':
            cliente.delete()
            messages.success(request, "Cliente eliminado.")
            return redirect('cliente_list')
    except ProtectedError:
        messages.error(request, "No se puede eliminar este cliente porque está asociado a registros de alquiler.")
        
    return render(request, 'cliente_confirm_delete.html', {
        'cliente': cliente,
        'breadcrumb_items': [('Clientes', f'Eliminar: {cliente.nombre}')],
    })


from cliente.models import Cliente

def obtener_o_crear_cliente_generico(empresa):
    cliente, creado = Cliente.objects.get_or_create(
        documento="0000",
        empresa=empresa,
        defaults={
            "nombre": "Cliente Genérico",
            "apellidos": "",
            "tipo_documento": "NI",
            "telefono": "",
            "correo": "generico@demo.com",
            "direccion": "Sin especificar",
            "estado": True
        }
    )
    return cliente

@login_required
def cliente_anular(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    try:
        if request.method == 'POST':
            cliente.delete()
            messages.success(request, "Cliente eliminado.")
            return redirect('cliente_list')
    except ProtectedError:
        messages.error(request, "No se puede eliminar este cliente porque está asociado a registros de alquiler.")
        
    return render(request, 'cliente_confirm_delete.html', {
        'cliente': cliente,
        'breadcrumb_items': [('Clientes', f'Eliminar: {cliente.nombre}')],
    })
