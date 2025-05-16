from django.urls import path
from alquiler.views_alquiler import buscar_clientes, editar_alquiler, crear_alquiler, eliminar_item_alquiler, buscar_productos, alquiler_list
from alquiler.views_impresion_alquiler import imprimir_alquiler

urlpatterns = [
    path('crear/', crear_alquiler, name='crear_alquiler'),
    path('editar/<int:pk>/', editar_alquiler, name='editar_alquiler'),
    path('eliminar-item/<int:pk>/', eliminar_item_alquiler, name='eliminar_item_alquiler'),
    path('', alquiler_list, name='alquiler_list'),
    path('productos-buscar/', buscar_productos, name='buscar_productos'),
    path('clientes-buscar/', buscar_clientes, name='buscar_clientes'),
    path('alquiler/<int:pk>/imprimir/', imprimir_alquiler, name='imprimir_alquiler'),

]
