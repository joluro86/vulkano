from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Proveedor
from producto.forms.forms_proveedor import ProveedorForm
from core.views import BreadcrumbMixin   
from django.contrib.auth.mixins import LoginRequiredMixin

class ProveedorListView(LoginRequiredMixin,BreadcrumbMixin, ListView):
    model = Proveedor
    template_name = 'proveedor_list.html'
    context_object_name = 'proveedores'
    ordering = ['nombre']
    paginate_by = 10
    breadcrumb_items = [
        ("Productos", reverse_lazy("producto_list")),
        ("Proveedores", None)
    ]
    
    def get_queryset(self):
        return Proveedor.objects.filter(empresa=self.request.user.empresa)
    
    
class ProveedorUpdateView(LoginRequiredMixin, BreadcrumbMixin, UpdateView):
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

class ProveedorCreateView(LoginRequiredMixin, BreadcrumbMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor_crear.html'
    success_url = reverse_lazy('proveedor_list')
    breadcrumb_items = [
        ("Proveedores", reverse_lazy("proveedor_list")),
        ("Crear", None)
    ]

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa 
        return super().form_valid(form)

        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Crear Proveedor',
            'boton_texto': 'Guardar Proveedor'
        })
        return context


