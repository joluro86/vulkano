from django.urls import path
from . import views

urlpatterns = [
    path('general/', views.informeGeneral, name='general'),
    path('productos/', views.informeProducto, name='producto'),
    path('clientes/', views.informeClientes, name='cliente'),
    path('alquileres/', views.informeAlquiler, name='alquiler'),
]