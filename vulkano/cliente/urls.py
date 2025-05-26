from django.urls import path
from cliente.views import cliente_list, cliente_create, cliente_delete, cliente_edit, cliente_list_por_estado

urlpatterns = [
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/por_estado/<str:estado>/', cliente_list_por_estado, name='cliente_list_por_estado'),
    path('clientes/crear/', cliente_create, name='cliente_create'),
    path('clientes/editar/<int:pk>/', cliente_edit, name='cliente_edit'),
    path('clientes/eliminar/<int:pk>/', cliente_delete, name='cliente_delete'),
]
