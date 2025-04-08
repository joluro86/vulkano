from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Producto
from producto.forms.forms_producto import ProductoForm
from core.views import BreadcrumbMixin

class ProductoCreateView(LoginRequiredMixin, BreadcrumbMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_form.html'
    success_url = reverse_lazy('producto_list')

    breadcrumb_items = [
        ("Productos", reverse_lazy("producto_list")),
        ("Crear", None)
    ]

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.creado_por = self.request.user
        form.instance.modificado_por = self.request.user
        return super().form_valid(form)
