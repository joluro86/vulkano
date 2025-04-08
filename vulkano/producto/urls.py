from django.urls import path
from producto.views_category import CategoriaListView, CategoriaCreateView, CategoriaUpdateView
from producto.views_proveedor import ProveedorListView, ProveedorCreateView, ProveedorUpdateView
urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('proveedores/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),
]
