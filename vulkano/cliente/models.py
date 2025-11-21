from django.db import models
from persona.models import Persona
from empresa.models import Empresa

class Cliente(Persona):
    documento = models.CharField(max_length=30) 
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        unique_together = ('documento', 'empresa') 

    def __str__(self):
        empresa_nombre = self.empresa.nombre if self.empresa else "Sin empresa"
        return f"{self.nombre} ({self.documento}) - {empresa_nombre}"
