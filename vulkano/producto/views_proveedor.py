from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Proveedor
from producto.forms.forms_proveedor import ProveedorForm
from core.views import BreadcrumbMixin   

class ProveedorListView(BreadcrumbMixin, ListView):
    model = Proveedor
    template_name = 'proveedor_list.html'
    context_object_name = 'proveedores'
    ordering = ['nombre']
    paginate_by = 10
    breadcrumb_items = [
        ("Productos", reverse_lazy("categoria_list")),
        ("Proveedores", None)
    ]
    
    
class ProveedorUpdateView(BreadcrumbMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor_crear.html'
    success_url = reverse_lazy('proveedor_list')
    breadcrumb_items = [
        ("Proveedores", reverse_lazy("proveedor_list")),
        ("Editar", None)
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Editar Proveedor',
            'boton_texto': 'Actualizar Proveedor'
        })
        return context

class ProveedorCreateView(BreadcrumbMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor_crear.html'
    success_url = reverse_lazy('proveedor_list')
    breadcrumb_items = [
        ("Proveedores", reverse_lazy("proveedor_list")),
        ("Crear", None)
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Crear Proveedor',
            'boton_texto': 'Guardar Proveedor'
        })
        return context


