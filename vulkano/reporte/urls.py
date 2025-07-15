# reporte/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('informe-ingresos/', views.informe_ingresos, name='informe_ingresos'),
]
