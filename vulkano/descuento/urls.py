# urls.py
from django.urls import path
from descuento.views import descuento_list, descuento_create, descuento_edit, descuento_delete

urlpatterns = [
    path('descuentos/', descuento_list, name='descuento_list'),
    path('descuentos/nuevo/', descuento_create, name='descuento_create'),
    path('descuentos/<int:pk>/editar/', descuento_edit, name='descuento_edit'),
    path('descuentos/<int:pk>/eliminar/', descuento_delete, name='descuento_delete'),
]
