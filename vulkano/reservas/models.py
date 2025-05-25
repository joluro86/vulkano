from django.db import models
from cliente.models import Cliente
from producto.models import Producto
from decimal import Decimal

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
        ('modificada', 'Modificada'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.precio:
            precio_obj = self.producto.precios.order_by('-id').first()
            if precio_obj:
                self.precio = precio_obj.valor

        if self.fecha_inicio and self.fecha_fin and self.precio:
            dias = (self.fecha_fin - self.fecha_inicio).days
            self.precio_total = Decimal(self.precio) * max(dias, 1)        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.id} - {self.producto.nombre} para {self.cliente.nombre} ({self.fecha_inicio} a {self.fecha_fin})"

