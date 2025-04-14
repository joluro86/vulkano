# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.db.models import Q
from empresa.models import Empresa, Sucursal
from empresa.forms.empresa_forms import EmpresaEditForm, SucursalForm, EmpresaForm, SucursalEditForm
from core.views import BreadcrumbMixin    
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import csv
from django.http import HttpResponse
from .models import Sucursal 
from .models import Empresa

class EmpresaCreateView(BreadcrumbMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'crear_empresa.html'
    success_url = reverse_lazy('empresa_list')
    breadcrumb_items = [ ("Empresas", reverse_lazy("empresa_list")),
            ("Crear", None)]  

class EmpresaListView(BreadcrumbMixin, ListView):
    model = Empresa
    template_name = "empresa_list.html"
    ordering = ['nombre'] 
    paginate_by = 10
    breadcrumb_items = [ ("Empresas", None), ]   

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

        estado = self.request.GET.get("estado")
        departamento = self.request.GET.get("departamento")
        ciudad = self.request.GET.get("ciudad")

        if estado:
            queryset = queryset.filter(estado=estado)
        if departamento:
            queryset = queryset.filter(departamento__icontains=departamento)
        if ciudad:
            queryset = queryset.filter(ciudad__icontains=ciudad)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = Empresa.ESTADOS
        context["ciudades"] = Empresa.objects.values_list("ciudad", flat=True).distinct().order_by("ciudad")
        context["departamentos"] = Empresa.objects.values_list("departamento", flat=True).distinct().order_by("departamento")
        return context

class EmpresaUpdateView(BreadcrumbMixin, UpdateView):
    model = Empresa
    form_class = EmpresaEditForm
    template_name = 'editar_empresa.html'
    success_url = reverse_lazy('empresa_list')
    breadcrumb_items = [  ("Empresas", reverse_lazy("empresa_list")),
            ("Editar", None) ]   

class SucursalCreateView(BreadcrumbMixin, CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'crear_sucursal.html'
    success_url = reverse_lazy('sucursal_list')

    breadcrumb_items = [
        ("Sucursales", reverse_lazy("sucursal_list")),
        ("Crear", None)
    ]

    def get_initial(self):
        initial = super().get_initial()
        empresa_id = self.request.GET.get("empresa")
        if empresa_id:
            initial["empresa"] = empresa_id
        return initial


class SucursalListView(BreadcrumbMixin, ListView):
    model = Sucursal
    template_name = 'sucursal_list.html'
    context_object_name = 'sucursales'
    ordering = ['nombre']  # Orden alfabético por nombre de sucursal
    paginate_by = 10
    breadcrumb_items = [("Empresas", reverse_lazy("empresa_list")),
                        ("Sucursales", None)]

    def get_queryset(self):
        # Opcional: Prefetch para optimizar consultas de empresa asociada
        #return super().get_queryset().select_related('empresa')

        queryset = super().get_queryset()
        estado = self.request.GET.get("estado")
        departamento = self.request.GET.get("departamento")
        ciudad = self.request.GET.get("ciudad")

        if estado:
            queryset = queryset.filter(estado=estado)
        if departamento:
            queryset = queryset.filter(departamento__icontains=departamento)
        if ciudad:
            queryset = queryset.filter(ciudad__icontains=ciudad)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = Sucursal.ESTADOS
        context["ciudades"] = Sucursal.objects.values_list("ciudad", flat=True).distinct().order_by("ciudad")
        context["departamentos"] = Sucursal.objects.values_list("departamento", flat=True).distinct().order_by("departamento")
        return context
       
class SucursalUpdateView(BreadcrumbMixin, UpdateView):
    model = Sucursal
    form_class = SucursalEditForm
    template_name = 'editar_sucursal.html'
    success_url = reverse_lazy('sucursal_list')
    breadcrumb_items = [
        ("Empresas", reverse_lazy("empresa_list")),
        ("Sucursales", reverse_lazy("sucursal_list")),
        ("Editar", None)]

class SucursalesPorEmpresaView(BreadcrumbMixin, ListView):
    model = Sucursal
    template_name = 'lista_sucursales_por_empresa.html'
    context_object_name = 'sucursales'
    breadcrumb_items = [("Empresas", reverse_lazy("empresa_list")),
                        ("Sucursales", None)]

    def get_queryset(self):
        self.empresa = get_object_or_404(Empresa, pk=self.kwargs['empresa_id'])
        return Sucursal.objects.filter(empresa=self.empresa)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa'] = self.empresa
        return context

def exportar_sucursales_csv(request):
    empresa_id = request.GET.get('empresa')
    if not empresa_id:
        return HttpResponse("ID de empresa no proporcionado", status=400)

    empresa = get_object_or_404(Empresa, pk=empresa_id)
    sucursales = Sucursal.objects.filter(empresa=empresa)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sucursales_{empresa.nombre}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Estado', 'Ciudad', 'Dirección', 'Departamento', 'Teléfono'])

    for s in sucursales:
        writer.writerow([
            s.nombre,
            s.get_estado_display(),
            s.ciudad,
            s.direccion,
            s.departamento,
            s.telefono,
        ])

    return response   

def exportar_empresas_csv(request):
    empresas = Empresa.objects.all()

    # Aplicar filtros si se usaron en el template
    estado = request.GET.get('estado')
    departamento = request.GET.get('departamento')
    ciudad = request.GET.get('ciudad')
    q = request.GET.get('q')

    if estado:
        empresas = empresas.filter(estado=estado)
    if departamento:
        empresas = empresas.filter(departamento=departamento)
    if ciudad:
        empresas = empresas.filter(ciudad=ciudad)
    if q:
        empresas = empresas.filter(
            nombre__icontains=q
        ) | empresas.filter(nit__icontains=q) | empresas.filter(
            direccion__icontains=q
        ) | empresas.filter(
            ciudad__icontains=q
        ) | empresas.filter(
            estado__icontains=q
        )

    # Generar respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="empresas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'NIT', 'Ciudad', 'Dirección', 'Departamento', 'Teléfono', 'Estado'])

    for e in empresas:
        writer.writerow([
            e.nombre,
            e.nit,
            e.ciudad,
            e.direccion,
            e.departamento,
            e.telefono,
            e.get_estado_display(),  # Si usas choices
        ])

    return response
    
