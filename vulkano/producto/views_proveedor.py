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
        ("Proveedores", None)
    ]
