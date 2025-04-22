from django.contrib import admin
from django.urls import path
from empresa.views import  SucursalesPorEmpresaView, EmpresaCreateView, EmpresaListView, EmpresaUpdateView, SucursalUpdateView, SucursalCreateView, SucursalListView, exportar_sucursales_csv, exportar_empresas

urlpatterns = [
    path('crear-empresa/', EmpresaCreateView.as_view(), name='crear_empresa'),
    path('empresas/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresas/editar/<int:pk>', EmpresaUpdateView.as_view(), name='editar_empresa'),
    
    path('empresas/<int:empresa_id>/sucursales/', SucursalesPorEmpresaView.as_view(), name='sucursales_por_empresa'),
    path('sucursales/', SucursalListView.as_view(), name='sucursal_list'),
    path('sucursales/crear/', SucursalCreateView.as_view(), name='crear_sucursal'),
    path('sucursales/<int:pk>/editar/', SucursalUpdateView.as_view(), name='editar_sucursal'),
    path('exportar_sucursales/', exportar_sucursales_csv, name='exportar_sucursales'),
    path('exportar_empresas/', exportar_empresas, name='exportar_empresas'),
]
