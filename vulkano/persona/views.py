from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Persona
from .forms import PersonaForm

@login_required
def persona_list(request):
    personas = Persona.objects.all().order_by('nombre')
    return render(request, 'persona_list.html', {
        'personas': personas,
        'breadcrumb_items': [('Personas', 'Listado')],
    })

@login_required
def persona_create(request):
    form = PersonaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Persona creada exitosamente.")
        return redirect('persona_list')
    
    return render(request, 'persona_form.html', {
        'form': form,
        'titulo': 'Crear persona',
        'boton_texto': 'Guardar persona',
        'breadcrumb_items': [('Personas', 'Crear')],
    })

@login_required
def persona_edit(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    form = PersonaForm(request.POST or None, instance=persona)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Persona actualizada exitosamente.")
        return redirect('persona_list')
    
    return render(request, 'persona_form.html', {
        'form': form,
        'titulo': 'Editar persona',
        'boton_texto': 'Actualizar persona',
        'breadcrumb_items': [('Personas', f'Editar: {persona.nombre}')],
    })

@login_required
def persona_delete(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        persona.delete()
        messages.success(request, "Persona eliminada.")
        return redirect('persona_list')
    
    return render(request, 'persona_confirm_delete.html', {
        'persona': persona,
        'breadcrumb_items': [('Personas', f'Eliminar: {persona.nombre}')],
    })
