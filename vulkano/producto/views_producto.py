from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Producto
from producto.forms.forms_producto import ProductoForm
from core.views import BreadcrumbMixin
from django.db.models import Q

@login_required
def eliminar_producto(request, id):
    Producto.objects.get(id=id).delete()
    return redirect('producto_list')

class ProductoCreateView(LoginRequiredMixin, BreadcrumbMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_crear.html'
    success_url = reverse_lazy('producto_list')

    breadcrumb_items = [
        ("Productos", reverse_lazy("producto_list")),
        ("Crear", None)
    ]

    def form_valid(self, form):
        usuario = self.request.user.get_full_name() or self.request.user.username

        if not form.instance.pk:
            form.instance.creado_por = usuario

        form.instance.modificado_por = usuario
        return super().form_valid(form)



class ProductoListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
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


class ProductoUpdateView(LoginRequiredMixin, BreadcrumbMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_crear.html'
    success_url = reverse_lazy('producto_list')

    breadcrumb_items = [
        ("Productos", reverse_lazy("producto_list")),
        ("Editar", None)
    ]

    def form_valid(self, form):
        form.instance.modificado_por = self.request.user.get_full_name() or self.request.user.username
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Producto"
        context['boton_texto'] = "Actualizar Producto"
        return context

class ProductoDetailView(LoginRequiredMixin, BreadcrumbMixin, DetailView):
    model = Producto
    template_name = 'producto_detalle.html'
    context_object_name = 'producto'

    breadcrumb_items = [
        ("Productos", reverse_lazy("producto_list")),
        ("Detalle", None)
    ]