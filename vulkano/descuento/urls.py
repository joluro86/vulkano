# urls.py
from django.urls import path
from descuento.views import descuento_list, descuento_create, descuento_edit, descuento_delete
from autenticacion.decorators import group_required
urlpatterns = [
    path('descuentos/', descuento_list, name='descuento_list'),
    path('descuentos/nuevo/',group_required('Administrador') (descuento_create), name='descuento_create'),
    path('descuentos/<int:pk>/editar/',group_required('Administrador') (descuento_edit), name='descuento_edit'),
    path('descuentos/<int:pk>/eliminar/',group_required('Administrador') (descuento_delete), name='descuento_delete'),
]
