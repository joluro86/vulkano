from django.urls import path
from autenticacion.views import landing_view, CustomLoginView, validar_username, crear_usuario, editar_usuario, usuario_list, registro_cliente
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static 
from django.conf import settings
from .decorators import group_required


urlpatterns = [
   path('', landing_view, name='landing'),
   path('login/', CustomLoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
   path('usuarios/crear/',group_required('Administrador') (crear_usuario), name='crear_usuario'),
   path('usuarios/editar/<int:pk>/',group_required('Administrador') (editar_usuario), name='editar_usuario'),
   path('usuarios/', usuario_list, name='usuario_list'),
   path('ajax/validar-username/', validar_username, name='validar_username'),
   path('registro/', registro_cliente, name='registro_cliente'),
]

urlpatterns+=static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)