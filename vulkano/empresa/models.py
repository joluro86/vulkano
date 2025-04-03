from django.db import models

class Empresa(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=50, unique=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="activo")

    def __str__(self):
        return self.nombre
