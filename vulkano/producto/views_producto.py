from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Producto
from producto.forms.forms_producto import ProductoForm
from core.views import BreadcrumbMixin
from django.db.models import Q
from producto.forms.forms_productos import BusquedaProductoForm
from django.shortcuts import get_object_or_404, redirect, render

def producto(request):
    form = BusquedaProductoForm(request.GET or None)
    productos = Producto.objects.all()

    if form.is_valid():
        marca = form.cleaned_data.get("marca")
        estado = form.cleaned_data.get("estado")
        ubicacion = form.cleaned_data.get("ubicacion_actual")

        if marca:
            productos = productos.filter(marca=marca)
        if estado:
            productos = productos.filter(estado=estado)
        if ubicacion:
            productos = productos.filter(ubicacion_actual=ubicacion)

    return render(request, "producto.html", {"form": form, "productos": productos})



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
            form.instance.empresa = self.request.user.empresa
            form.instance.sucursal = self.request.user.sucursal

        form.instance.modificado_por = usuario
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



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
        queryset = Producto.objects.por_empresa(self.request.user.empresa)
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
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ProductoDetailView(LoginRequiredMixin, BreadcrumbMixin, DetailView):
    model = Producto
    template_name = 'producto_detalle.html'
    context_object_name = 'producto'

    breadcrumb_items = [
        ("Productos", reverse_lazy("producto_list")),
        ("Detalle", None)
    ]