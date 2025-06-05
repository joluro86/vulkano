from django.urls import path
from alquiler.views_alquiler import ver_alquiler, limpiar_descuento, anular_alquiler, liquidar_alquiler, aplicar_descuento_alquiler, buscar_clientes, editar_alquiler, crear_alquiler, eliminar_item_alquiler, buscar_productos, alquiler_list
from alquiler.views_impresion_alquiler import imprimir_alquiler

urlpatterns = [
    path('crear/', crear_alquiler, name='crear_alquiler'),
    path('editar/<int:pk>/', editar_alquiler, name='editar_alquiler'),
    path('eliminar-item/<int:pk>/', eliminar_item_alquiler, name='eliminar_item_alquiler'),
    path('', alquiler_list, name='alquiler_list'),
    path('productos-buscar/', buscar_productos, name='buscar_productos'),
    path('clientes-buscar/', buscar_clientes, name='buscar_clientes'),
    path('alquiler/<int:pk>/imprimir/', imprimir_alquiler, name='imprimir_alquiler'),
    path('alquiler/<int:pk>/aplicar-descuento/', aplicar_descuento_alquiler, name='aplicar_descuento_alquiler'),
    path('alquiler/<int:pk>/quitar-descuento/', limpiar_descuento, name='limpiar_descuentos'),
    path('anular/<int:pk>/', anular_alquiler, name="anular_alquiler"),
    path('liquidar/<int:pk>/', liquidar_alquiler, name="liquidar_alquiler"),
    path('ver/<int:pk>/', ver_alquiler, name='ver_alquiler'),
    path('imprimir/<int:pk>/', imprimir_alquiler, name='imprimir_alquiler'),
]
