# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.db.models import Q
from empresa.models import Empresa, Sucursal
from empresa.logic.empresa_logic import create_empresa
from empresa.forms.empresa_forms import EmpresaEditForm, SucursalForm, EmpresaForm, SucursalEditForm

class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'crear_empresa.html'
    success_url = reverse_lazy('empresa_list')

    def form_valid(self, form):
        # Aquí llamamos la creación de la empresa a nuestro logic
        create_empresa(form)
        return super().form_valid(form)

class EmpresaListView(ListView):
    model = Empresa
    template_name = "empresa_list.html"
    ordering = ['nombre'] 
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(nit__icontains=query) |
                Q(ciudad__icontains=query) |
                Q(departamento__icontains=query) |
                Q(estado__icontains=query) |
                Q(direccion__icontains=query)  # Puedes agregar más filtros si es necesario
            )
        return queryset

class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaEditForm
    template_name = 'editar_empresa.html'
    success_url = reverse_lazy('empresa_list')


class SucursalCreateView(CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'crear_sucursal.html'
    success_url = reverse_lazy('sucursal_list')
    

class SucursalListView(ListView):
    model = Sucursal
    template_name = 'sucursal_list.html'
    context_object_name = 'sucursales'
    ordering = ['nombre']  # Orden alfabético por nombre de sucursal
    paginate_by = 10

    def get_queryset(self):
        # Opcional: Prefetch para optimizar consultas de empresa asociada
        return super().get_queryset().select_related('empresa')

class SucursalUpdateView(UpdateView):
    model = Sucursal
    form_class = SucursalEditForm
    template_name = 'editar_sucursal.html'
    success_url = reverse_lazy('sucursal_list')
