from django.urls import path
from . import views

urlpatterns = [
    path('general/', views.informeGeneral, name='general'),
    path('productos/', views.informeProducto, name='producto'),
]