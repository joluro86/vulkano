from alquiler.models import EventoAlquiler

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
