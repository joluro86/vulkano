from django.urls import path
from .views import show_rooms, join_room, mi_sala_chat, cerrar_sala
from autenticacion.decorators import group_required

urlpatterns = [
    path('rooms/', show_rooms, name='room_list'),
    path('rooms/<slug:room_slug>/', join_room, name='room_detail'),
    path('mi-chat/', mi_sala_chat, name='mi_sala_chat'),
    path('rooms/<slug:room_slug>/cerrar/', cerrar_sala, name='cerrar_sala'),  
]

