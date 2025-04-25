from django.urls import path
from .views import LoginMFAView, VerifyMFAView, editar_usuario_view, bienvenida_view, crear_usuario_view, registro_view, administrar_usuarios_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login-mfa/', LoginMFAView.as_view(), name='login_mfa'),
    path('verify-mfa/', VerifyMFAView.as_view(), name='verify_mfa'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', bienvenida_view, name='bienvenida'),
    path('registro/', registro_view, name='registro'),
    path('usuarios/', administrar_usuarios_view, name='administrar_usuarios'),
    path('usuarios/crear/', crear_usuario_view, name='crear_usuario'),
    path('usuarios/<int:perfil_id>/editar/', editar_usuario_view, name='editar_usuario'),
    
]
