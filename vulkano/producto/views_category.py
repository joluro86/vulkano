from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Categoria
from producto.forms.forms_category import CategoriaForm
from core.views import BreadcrumbMixin    


class CategoriaListView(BreadcrumbMixin, ListView):
    model = Categoria
    template_name = 'categoria_list.html'
    context_object_name = 'categorias'
    ordering = ['nombre']
    paginate_by = 10
    breadcrumb_items = [
        ("Productos", reverse_lazy("categoria_list")),
        ("Categorías", None)
    ]

class CategoriaCreateView(BreadcrumbMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria_crear.html'
    success_url = reverse_lazy('categoria_list')
    breadcrumb_items = [
        ("Productos", reverse_lazy("categoria_list")),
        ("Categorías", reverse_lazy("categoria_list")),
        ("Crear", None)
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Crear Categoría',
            'boton_texto': 'Guardar Categoría'
        })
        return context

class CategoriaUpdateView(BreadcrumbMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria_crear.html'
    success_url = reverse_lazy('categoria_list')
    breadcrumb_items = [
        ("Productos", reverse_lazy("categoria_list")),
        ("Categorías", reverse_lazy("categoria_list")),
        ("Editar", None)
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Editar Categoría',
            'boton_texto': 'Actualizar Categoría'
        })
        return context
