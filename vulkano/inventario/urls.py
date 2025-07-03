# inventario/urls.py

from django.urls import path
from .views_stock import inventario_list_view

urlpatterns = [
    path('stock/', inventario_list_view, name='inventario_list_stock'),
]

