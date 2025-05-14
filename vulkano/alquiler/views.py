from django.views.generic import ListView
from producto.models import Producto # Importa el modelo Producto
from core.views import BreadcrumbMixin # Importación corregida según tu comentario
from datetime import date # Importar date para manejar fechas

# Define un precio fijo por día para todos los productos por ahora
PRECIO_FIJO_POR_DIA = 100

class ProductosAlquilerListView(BreadcrumbMixin, ListView):
    """
    Vista para listar productos disponibles para alquiler.
    Muestra un checkbox, imagen, nombre, descripción y campos de fecha
    para cada producto. Maneja GET para mostrar la lista y POST para
    previsualizar el costo del alquiler.
    """
    model = Producto
    template_name = 'alquiler/productos_alquiler.html'
    context_object_name = 'productos'
    ordering = ['nombre']
    paginate_by = 9 # Añadimos paginación, 9 elementos por página

    breadcrumb_items = [
        ("Inicio", "/"),
        ("Alquiler de Productos", None)
    ]

    def get_queryset(self):
        """
        Retorna el queryset de productos. Por ahora, listamos todos.
        """
        queryset = super().get_queryset()
        # Si necesitas filtrar por disponibilidad en el futuro:
        # queryset = queryset.filter(estado='disponible')
        # Si tienes búsqueda en GET como en producto_list:
        # q = self.request.GET.get('q')
        # if q:
        #     queryset = queryset.filter(
        #         Q(nombre__icontains=q) |
        #         Q(codigo_interno__icontains=q) |
        #         Q(ubicacion_actual__icontains=q)
        #     )
        return queryset

    def post(self, request, *args, **kwargs):
        """
        Maneja la solicitud POST para previsualizar el costo del alquiler.
        """
        # Obtener los IDs de los productos seleccionados
        productos_seleccionados_ids = request.POST.getlist('productos_seleccionados')

        # Obtener las fechas de inicio y fin
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')

        costo_total = None
        duracion_dias = 0
        date_errors = None # Variable para almacenar errores de fecha

        # Validar y procesar las fechas si están presentes
        if fecha_inicio_str and fecha_fin_str:
            try:
                fecha_inicio = date.fromisoformat(fecha_inicio_str)
                fecha_fin = date.fromisoformat(fecha_fin_str)

                # Validar que la fecha de fin no sea anterior a la de inicio
                if fecha_fin < fecha_inicio:
                    date_errors = "La fecha de fin no puede ser anterior a la fecha de inicio."
                else:
                    # Calcular la duración en días (incluyendo ambos días)
                    duracion = fecha_fin - fecha_inicio
                    duracion_dias = duracion.days + 1 # Sumar 1 para incluir el día de fin

                    # Calcular el costo total si hay productos seleccionados
                    if productos_seleccionados_ids:
                        productos_seleccionados_count = len(productos_seleccionados_ids)
                        costo_total = productos_seleccionados_count * duracion_dias * PRECIO_FIJO_POR_DIA
                    else:
                         # Si no hay productos seleccionados, el costo es 0, pero aún mostramos el resumen de fechas
                         costo_total = 0

            except ValueError:
                # Manejar errores si las fechas no tienen el formato correcto
                date_errors = "Formato de fecha inválido."
        elif productos_seleccionados_ids:
             # Si se seleccionaron productos pero faltan fechas
             date_errors = "Por favor, selecciona las fechas de inicio y fin del alquiler."

        response = self.get(request, *args, **kwargs)

        context = response.context_data

        # Ahora, actualizamos el contexto con los datos específicos del POST
        context['productos_seleccionados_ids'] = productos_seleccionados_ids
        context['fecha_inicio_str'] = fecha_inicio_str
        context['fecha_fin_str'] = fecha_fin_str
        context['duracion_dias'] = duracion_dias
        context['costo_total'] = costo_total
        context['date_errors'] = date_errors
        context['productos_seleccionados_count'] = len(productos_seleccionados_ids) if productos_seleccionados_ids else 0

        # Renderizar la respuesta que ya fue preparada por get() pero con el contexto actualizado
        return response


    # Sobrescribir get_context_data para asegurar que breadcrumb_items esté siempre disponible
    # y para pasar object_list correctamente
    def get_context_data(self, **kwargs):
        # Llama al método get_context_data de la clase padre (ListView y BreadcrumbMixin)
        # para obtener el contexto base, incluyendo la paginación y object_list.
        context = super().get_context_data(**kwargs)

        # Añade los breadcrumb_items al contexto
        context['breadcrumb_items'] = self.breadcrumb_items

        # Asegurarse de que 'productos_seleccionados_ids' esté en el contexto
        # incluso en una solicitud GET inicial (aunque estará vacío).
        # Esto evita errores en el template al iterar sobre él.
        if 'productos_seleccionados_ids' not in context:
             context['productos_seleccionados_ids'] = []

        return context

