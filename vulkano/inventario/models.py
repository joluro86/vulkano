from django.db import models
from producto.models import Producto, Proveedor
from empresa.models import Sucursal
from vulkano import settings
from cliente.models import Cliente
from django.db import models
from alquiler.models import Alquiler
class InventarioSucursal(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventarios')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='inventarios')
    total_historico = models.IntegerField(default=0)
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

class MovimientoInventario(models.Model):
    TIPOS = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('devolucion', 'Devolución'),
        ('ajuste', 'Ajuste manual'),
    ]
    
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('anulado', 'Anulado'),
    ]

    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True)

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_creados_por')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_actualizados_por')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'

    def __str__(self):
        return f"{self.tipo} - {self.sucursal.nombre} - {self.fecha.date()}"

class MovimientoItem(models.Model):
    movimiento = models.ForeignKey(
        'inventario.MovimientoInventario',
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Ítem de movimiento'
        verbose_name_plural = 'Ítems de movimiento'

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

class ReservaInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='reservas')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='reservas')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='reservas')
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE, related_name='reservas')
    cantidad_reservada = models.PositiveIntegerField()
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    entregado = models.BooleanField(default=False, help_text="Se marca como entregado cuando el producto se entregue")

    class Meta:
        unique_together = ('producto', 'alquiler')
        verbose_name = 'Reserva de Inventario'
        verbose_name_plural = 'Reservas de Inventario'

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_reservada} reservadas para {self.cliente.nombre}"
