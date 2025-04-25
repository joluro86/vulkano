from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import random

User = get_user_model()

class TwoFactorCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @classmethod
    def create_for_user(cls, user, minutes=5):
        code = f"{random.randint(0,999999):06d}"
        expires = datetime.now() + timedelta(minutes=minutes)
        return cls.objects.create(user=user, code=code, expires_at=expires)

    def is_valid(self):
        return datetime.now() < self.expires_at

# auth/models.py

from django.contrib.auth.models import User
from django.db import models
from empresa.models import Sucursal  # Asegúrate de importar tu modelo Sucursal

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    ROLES = [
        ('admin', 'Administrador de Empresa'),
        ('bodega', 'Encargado de Bodega'),
        ('tecnico', 'Técnico de Campo'),
        ('consulta', 'Consulta'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()} - {self.sucursal.nombre}"
