from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# Asumiendo que BreadcrumbMixin está en algún lugar que importas
from core.views import BreadcrumbMixin

from .models import Producto, InventarioProducto # Asegúrate de importar InventarioProducto

class ProductoListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
    model = Producto
    template_name = 'inventario_productos.html'
    context_object_name = 'productos'
    ordering = ['nombre']
    paginate_by = 9  # o lo que prefieras

    breadcrumb_items = [
        ("Productos", None)
    ]

    def get_queryset(self):
        queryset = Producto.objects.por_empresa(self.request.user.empresa)
        q = self.request.GET.get('q')
        
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(codigo_interno__icontains=q) |
                Q(ubicacion_actual__icontains=q)
            )
        return queryset
