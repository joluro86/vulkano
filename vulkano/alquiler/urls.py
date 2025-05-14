from django.urls import path
from .views import ProductosAlquilerListView

# Define el namespace para esta app
app_name = 'alquiler'

urlpatterns = [
    # URL para la vista de listado de productos para alquiler
    path('productos/', ProductosAlquilerListView.as_view(), name='lista_productos_alquiler'),
    # Aquí podrías añadir más URLs relacionadas con el proceso de alquiler
    # path('confirmar/', ConfirmarAlquilerView.as_view(), name='confirmar_alquiler'),
]

