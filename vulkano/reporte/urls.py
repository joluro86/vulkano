# reporte/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('informe-ingresos/', views.informe_ingresos, name='informe_ingresos'),
    path('informe-economico_alquileres/', views.informe_economico, name='informe_economico_alquileres'),
]
