from alquiler.models import EventoAlquiler
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from alquiler.models import Alquiler

def registrar_evento_alquiler(alquiler, tipo, descripcion='', valor=None, estado_asociado='', usuario=None):
    """
    Registra un evento relacionado con un alquiler.
    
    Parámetros:
    - alquiler: instancia del alquiler
    - tipo: tipo de evento ('estado', 'abono', 'salida', 'devolucion', 'nota')
    - descripcion: detalle del evento
    - valor: valor monetario asociado (ej: abono)
    - estado_asociado: nuevo estado si tipo = 'estado'
    - usuario: usuario que realizó la acción
    """
    return EventoAlquiler.objects.create(
        alquiler=alquiler,
        tipo=tipo,
        descripcion=descripcion,
        valor=valor,
        estado_asociado=estado_asociado,
        creado_por=usuario
    )

def descontar_del_inventario(cantidad):
    pass



@login_required
def anular_alquiler(request, pk):
    alquiler = get_object_or_404(
        Alquiler, pk=pk, usuario__empresa=request.user.empresa
    )

    alquiler.estado = 'anulado'  # <- aquí va '=' no '=='
    alquiler.save()

    messages.success(request, f"El alquiler #{alquiler.id} ha sido anulado correctamente.")
    return redirect('editar_alquiler', pk=pk)
