from django.urls import path
from persona.views import persona_list, persona_edit, persona_create, persona_delete

urlpatterns = [
    path('personas/', persona_list, name='persona_list'),
    path('personas/crear/', persona_create, name='persona_create'),
    path('personas/editar/<int:pk>/', persona_edit, name='persona_edit'),
    path('personas/eliminar/<int:pk>/', persona_delete, name='persona_delete'),
]
