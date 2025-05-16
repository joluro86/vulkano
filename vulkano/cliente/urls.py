from django.urls import path
from cliente.views import cliente_list, cliente_create, cliente_delete, cliente_edit 

urlpatterns = [
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/crear/', cliente_create, name='cliente_create'),
    path('clientes/editar/<int:pk>/', cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:pk>/', cliente_delete, name='cliente_delete'),
]
