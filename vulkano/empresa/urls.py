from django.contrib import admin
from django.urls import path, include
from empresa.views import EmpresaCreateView, EmpresaListView

urlpatterns = [
    path('crear-empresa/', EmpresaCreateView.as_view(), name='crear_empresa'),
    path('empresas/', EmpresaListView.as_view(), name='empresa_list'),
]