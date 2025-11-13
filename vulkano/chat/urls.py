from django.urls import path
from .views import show_rooms, join_room

urlpatterns = [
    path('rooms/', show_rooms, name='room_list'),
    path('rooms/<slug:room_slug>/', join_room, name='room_detail'),
    
]

