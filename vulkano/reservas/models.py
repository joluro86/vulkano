from django.db import models
from cliente.models import Cliente
from producto.models import Producto

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

    def __str__(self):
        return f"Reserva {self.id} - {self.producto.nombre} para {self.cliente.nombre} ({self.fecha_inicio} a {self.fecha_fin})"

