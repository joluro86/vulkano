# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.db.models import Q
from empresa.models import Empresa, Sucursal
from empresa.forms.empresa_forms import EmpresaEditForm, SucursalForm, EmpresaForm, SucursalEditForm
from core.views import BreadcrumbMixin    
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv
import io
import openpyxl 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class EmpresaCreateView(LoginRequiredMixin, BreadcrumbMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'crear_empresa.html'
    success_url = reverse_lazy('empresa_list')
    breadcrumb_items = [ ("Empresas", reverse_lazy("empresa_list")),
            ("Crear", None)]  

class EmpresaListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
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

class EmpresaUpdateView(LoginRequiredMixin, BreadcrumbMixin, UpdateView):
    model = Empresa
    form_class = EmpresaEditForm
    template_name = 'editar_empresa.html'
    success_url = reverse_lazy('empresa_list')
    breadcrumb_items = [  ("Empresas", reverse_lazy("empresa_list")),
            ("Editar", None) ]   

class SucursalCreateView(LoginRequiredMixin, BreadcrumbMixin, CreateView):
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


class SucursalListView(LoginRequiredMixin, BreadcrumbMixin, ListView):
    model = Sucursal
    template_name = 'sucursal_list.html'
    ordering = ['nombre']  # Orden alfabético por nombre de sucursal
    paginate_by = 10
    breadcrumb_items = [("Empresas", reverse_lazy("empresa_list")),
                        ("Sucursales", None)]

    def get_queryset(self):
        # Opcional: Prefetch para optimizar consultas de empresa asociada
        #return super().get_queryset().select_related('empresa')

        queryset = super().get_queryset()

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(empresa__nombre__icontains=query) |
                Q(ciudad__icontains=query) |
                Q(departamento__icontains=query) |
                Q(telefono__icontains=query) |
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
        context["estados"] = Sucursal.ESTADOS
        context["ciudades"] = Sucursal.objects.values_list("ciudad", flat=True).distinct().order_by("ciudad")
        context["departamentos"] = Sucursal.objects.values_list("departamento", flat=True).distinct().order_by("departamento")
        context['sucursales'] = Sucursal.objects.filter(empresa=self.request.user.empresa)
        return context
       
class SucursalUpdateView(LoginRequiredMixin, BreadcrumbMixin, UpdateView):
    model = Sucursal
    form_class = SucursalEditForm
    template_name = 'editar_sucursal.html'
    success_url = reverse_lazy('sucursal_list')
    breadcrumb_items = [
        ("Empresas", reverse_lazy("empresa_list")),
        ("Sucursales", reverse_lazy("sucursal_list")),
        ("Editar", None)]

class SucursalesPorEmpresaView(LoginRequiredMixin, BreadcrumbMixin, ListView):
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
    
@login_required
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

@login_required
def exportar_empresas(request):
    tipo = request.GET.get('tipo', 'csv')  # por defecto CSV
    filtros = {}
    estado = request.GET.get('estado')
    departamento = request.GET.get('departamento')
    ciudad = request.GET.get('ciudad')
    q = request.GET.get('q')

    if estado:
        filtros['estado'] = estado
    if departamento:
        filtros['departamento'] = departamento
    if ciudad:
        filtros['ciudad'] = ciudad

    empresas = Empresa.objects.filter(**filtros)

    if q:
        empresas = empresas.filter(
            Q(nombre__icontains=q) |
            Q(nit__icontains=q) |
            Q(direccion__icontains=q) |
            Q(ciudad__icontains=q) |
            Q(estado__icontains=q)
        )

    columnas = ['Nombre', 'NIT', 'Ciudad', 'Dirección', 'Departamento', 'Teléfono', 'Estado']

    if tipo == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="empresas.csv"'
        response.write('\ufeff')  # BOM para Excel
        writer = csv.writer(response)
        writer.writerow(columnas)
        for e in empresas:
            writer.writerow([
                e.nombre, e.nit, e.ciudad, e.direccion,
                e.departamento, e.telefono,
                e.get_estado_display() if hasattr(e, 'get_estado_display') else e.estado
            ])
        return response

    elif tipo == 'txt':
        response = HttpResponse(content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="empresas.txt"'
        response.write('\ufeff')
        response.write('\t'.join(columnas) + '\n')
        for e in empresas:
            fila = [
                e.nombre, e.nit, e.ciudad, e.direccion,
                e.departamento, e.telefono,
                e.get_estado_display() if hasattr(e, 'get_estado_display') else e.estado
            ]
            response.write('\t'.join(map(str, fila)) + '\n')
        return response

    elif tipo == 'excel':
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Empresas'
        ws.append(columnas)
        for e in empresas:
            ws.append([
                e.nombre, e.nit, e.ciudad, e.direccion,
                e.departamento, e.telefono,
                e.get_estado_display() if hasattr(e, 'get_estado_display') else e.estado
            ])
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="empresas.xlsx"'
        return response

    else:
        return HttpResponse("Tipo de exportación no válido.", status=400)
