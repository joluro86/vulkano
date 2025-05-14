from django.urls import path
from autenticacion.views import landing_view, CustomLoginView, crear_usuario, editar_usuario, usuario_list
from django.contrib.auth.views import LogoutView

urlpatterns = [
   path('', landing_view, name='landing'),
   path('login/', CustomLoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
   path('usuarios/crear/', crear_usuario, name='crear_usuario'),
   path('usuarios/editar/<int:pk>/', editar_usuario, name='editar_usuario'),
   path('usuarios/', usuario_list, name='usuario_list'),
]
