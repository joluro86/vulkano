from django.db import models

class Descuento(models.Model):
    TIPO_CHOICES = [
        ('general', 'Descuento general al alquiler'),
        ('por_producto', 'Descuento aplicado a productos'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, help_text="Ej. 10 para 10%")
    activo = models.BooleanField(default=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%) - {self.get_tipo_display()}"

