from django.db import models
from django.conf import settings
from cliente.models import Cliente
class Alquiler(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='alquileres', null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='alquileres_creados_por'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='alquileres_actualizados_por'
    )

    def __str__(self):
        return f"Alquiler #{self.id} - {self.usuario}"


class AlquilerItem(models.Model):
    alquiler = models.ForeignKey('Alquiler', on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('producto.Producto', on_delete=models.CASCADE)
    dias_a_cobrar = models.PositiveIntegerField(null=True, blank=True)
    precio_dia = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    valor_item = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Calcular días automáticamente si no se digitó
        if not self.dias_a_cobrar and self.alquiler.fecha_inicio and self.alquiler.fecha_fin:
            self.dias_a_cobrar = (self.alquiler.fecha_fin - self.alquiler.fecha_inicio).days + 1

        # En caso de que aún esté vacío (sin fechas), por defecto
        if not self.dias_a_cobrar:
            self.dias_a_cobrar = 1

        # Calcular el valor total del ítem
        self.valor_item = self.dias_a_cobrar * self.precio_dia
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto} ({self.dias_a_cobrar} días a {self.precio_dia} c/u)"
