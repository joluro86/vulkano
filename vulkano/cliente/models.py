from django.db import models
from persona.models import Persona
from empresa.models import Empresa

class Cliente(Persona):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre

