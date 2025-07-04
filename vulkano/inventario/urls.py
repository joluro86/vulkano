# inventario/urls.py

from django.urls import path
from .views_stock import inventario_list_view
from .views_movimiento import crear_movimiento, movimiento_list, editar_movimiento, ver_movimiento

urlpatterns = [
    path('stock/', inventario_list_view, name='inventario_list_stock'),
    path('movimientos/nuevo/', crear_movimiento, name='crear_movimiento'),
    
    path('movimientos/', movimiento_list, name='movimiento_list'),
    path('movimientos/<int:pk>/editar/', editar_movimiento, name='editar_movimiento'),
    path('movimientos/<int:pk>/', ver_movimiento, name='ver_movimiento'),
]


