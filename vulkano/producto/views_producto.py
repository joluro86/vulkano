from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView
from .models import Producto
from producto.forms.forms_producto import ProductoForm
from core.views import BreadcrumbMixin
from django.db.models import Q

class ProductoCreateView(BreadcrumbMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_crear.html'
    success_url = reverse_lazy('producto_list')

    breadcrumb_items = [
        ("Productos", reverse_lazy("producto_list")),
        ("Crear", None)
    ]

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.creado_por = "null"
        form.instance.modificado_por = "null"
        return super().form_valid(form)


class ProductoListView(BreadcrumbMixin, ListView):
    model = Producto
    template_name = 'producto_list.html'
    context_object_name = 'productos'
    ordering = ['nombre']
    paginate_by = 9  # o lo que prefieras

    breadcrumb_items = [
        ("Productos", None)
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q) |
                Q(codigo_interno__icontains=q) |
                Q(ubicacion_actual__icontains=q)
            )
        return queryset


