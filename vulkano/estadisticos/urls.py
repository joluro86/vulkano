from django.urls import path
from . import views
from . import views_pdf

urlpatterns = [
    path('general/', views.informeGeneral, name='general'),
    path('productos/', views.informeProducto, name='producto'),
    path('clientes/', views.informeClientes, name='cliente'),
    path('alquileres/', views.informeAlquiler, name='alquiler'),
    path('estadisticos/imprimir/', views_pdf.imprimir_estadistico, name='imprimir_estadistico'),
    path('general/imprimir/', views_pdf.imprimir_general, name='imprimir_general'),
    path('producto/imprimir/', views_pdf.imprimir_producto, name='imprimir_producto'),
    path('estadisticos/clientes/imprimir/', views_pdf.generar_pdf_clientes, name='imprimir_clientes'),
]