from django.urls import path
from alquiler.views_alquiler import editar_alquiler, crear_alquiler, eliminar_item_alquiler

urlpatterns = [
    path('crear/', crear_alquiler, name='crear_alquiler'),
    path('editar/<int:pk>/', editar_alquiler, name='editar_alquiler'),
    path('eliminar-item/<int:pk>/', eliminar_item_alquiler, name='eliminar_item_alquiler'),
    path('', editar_alquiler, name='alquiler_list'),
]
