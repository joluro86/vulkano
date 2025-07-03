from django.db import models
from producto.models import Producto
from empresa.models import Sucursal

class InventarioSucursal(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventarios')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='inventarios')
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0, help_text="Nivel mínimo recomendado para alertas")
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    bloqueado = models.BooleanField(default=False, help_text="Si está activo, el producto no se puede usar")

    class Meta:
        unique_together = ('producto', 'sucursal')
        verbose_name = 'Inventario por Sucursal'
        verbose_name_plural = 'Inventarios por Sucursal'

    def __str__(self):
        return f"{self.producto.nombre} - {self.sucursal.nombre}: {self.stock_actual} unidades"
