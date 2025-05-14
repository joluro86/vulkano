from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from empresa.models import Empresa, Sucursal

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)

    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default="activo")

    foto_perfil = models.ImageField(upload_to='usuarios/img/', blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='usuarios',  # Evita conflicto con 'user_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios',  # Evita conflicto con 'user_set'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


