from django.urls import path
from inventario.views_reserva import listar_reservas
from .views_stock import inventario_list_stock, limpiar_inventario
from .views_movimiento import crear_movimiento, confirmar_movimiento, movimiento_list, editar_movimiento, ver_movimiento, eliminar_item_movimiento

urlpatterns = [
    path('stock/', inventario_list_stock, name='inventario_list_stock'),
    path('movimientos/nuevo/', crear_movimiento, name='crear_movimiento'),
    
    path('movimientos/', movimiento_list, name='movimiento_list'),
    path('movimientos/<int:pk>/editar/', editar_movimiento, name='editar_movimiento'),
    path('movimientos/<int:pk>/', ver_movimiento, name='ver_movimiento'),
    path('movimientos/item/eliminar/<int:pk>/', eliminar_item_movimiento, name='eliminar_item_movimiento'),
    path('movimiento/<int:pk>/confirmar/', confirmar_movimiento, name='confirmar_movimiento'),
    path('reservas/', listar_reservas, name='listado_reservas'),
    
    path('limpiar_inventario/', limpiar_inventario, name='limpiar_inventario'),
]


