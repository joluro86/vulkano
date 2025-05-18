from django.urls import path
from .views import ReservaListView, ReservaCreateView, ReservaUpdateView
from . import views

urlpatterns = [
    path('solicitudes/', ReservaListView.as_view(), name='solicitudes_reserva'),
    path('solicitudes/crear/', ReservaCreateView.as_view(), name='crear_reserva'),
    path('solicitudes/editar/<int:pk>/', ReservaUpdateView.as_view(), name='editar_reserva'),
    path('cotizaciones/', views.cotizaciones_view, name='reservas_cotizaciones'),
    path('calendario/', views.calendario_view, name='reservas_calendario'),
]

