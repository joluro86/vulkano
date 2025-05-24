from django.urls import path
from producto.views_category import CategoriaListView, CategoriaCreateView, CategoriaUpdateView
from producto.views_proveedor import ProveedorListView, ProveedorCreateView, ProveedorUpdateView
from producto.views_producto import eliminar_producto, ProductoCreateView, ProductoListView, ProductoUpdateView, ProductoDetailView
from producto.views_precios import precio_producto_create, precio_producto_delete, precio_producto_list, precio_producto_edit
urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/crear/', CategoriaCreateView.as_view(), name='crear_categoria'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('proveedores/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/crear/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),
    
    path('catalogo/', ProductoListView.as_view(), name='producto_list'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('detalles/<int:pk>/', ProductoDetailView.as_view(), name='detalle_producto'),
    path('eliminar/<int:id>', eliminar_producto, name="eliminar_producto"),
    
    path('precios/', precio_producto_list, name='precio_producto_list'),
    path('precios/crear/', precio_producto_create, name='precio_producto_create'),
    path('precios/editar/<int:pk>/', precio_producto_edit, name='precio_producto_edit'),
    path('precios/eliminar/<int:pk>/', precio_producto_delete, name='precio_producto_delete'),

]
