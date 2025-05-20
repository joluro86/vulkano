from django.db import models
from persona.models import Persona
from empresa.models import Empresa

class Cliente(Persona):
    documento = models.CharField(max_length=30)  # ← ahora está en Cliente
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        unique_together = ('documento', 'empresa')  # ✅ ahora sí funciona

    def __str__(self):
        return f"{self.nombre} ({self.documento}) - {self.empresa.nombre}"
