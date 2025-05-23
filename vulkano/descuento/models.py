from django.db import models

from empresa.models import Empresa

class Descuento(models.Model):
    TIPO_CHOICES = [
        ('oferta', 'Oferta'),
        ('convenio', 'Convenio'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, help_text="Ej. 10 para 10%")
    activo = models.BooleanField(default=True)
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='descuentos', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creado_por = models.CharField(max_length=100, blank=True, null=True)
    modificado_por = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%) - {self.get_tipo_display()}"

