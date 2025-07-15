from django.db import models
from django.conf import settings
from cliente.models import Cliente
from decimal import Decimal
from producto.models import PrecioProducto

class Alquiler(models.Model):

    ESTADOS_ALQUILER = [
        ('cotizacion', 'Cotización'),
        ('borrador', 'Borrador'),
        ('reservado', 'Reservado'),
        ('despachado', 'Despachado'),
        ('liquidado', 'Liquidado'),
        ('anulado', 'Anulado'),
    ]
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name='alquileres', null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0,
        help_text="Total cobro del alquiler"
    )

    estado = models.CharField(
        max_length=20, choices=ESTADOS_ALQUILER, default='borrador')

    descuento_general = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0,
        help_text="Descuento general en % sobre el total del alquiler"
    )

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

    @property
    def total_sin_descuento(self):
        return sum(item.valor_item for item in self.items.all())

    @property
    def total_con_descuento(self):
        total = self.total_sin_descuento
        descuento = total * (self.descuento_general / Decimal('100'))
        return total - descuento

    @property
    def total_abonado(self):
        return sum(a.valor for a in self.abonos.all())

    @property
    def saldo_pendiente(self):
        return max(self.total_con_descuento - self.total_abonado, 0)

    @property
    def puede_liquidarse(self):
        return self.estado != 'liquidado' and self.saldo_pendiente == 0

class AlquilerItem(models.Model):
    alquiler = models.ForeignKey(
        'Alquiler', on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('producto.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=True, blank=True, default=1)
    dias_a_cobrar = models.PositiveIntegerField(null=True, blank=True)
    precio_dia = models.DecimalField(max_digits=10, decimal_places=2)
    valor_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    descuento_porcentaje = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0,
        help_text="Descuento individual en % (ej. 10 para 10%)"
    )
    valor_item = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.dias_a_cobrar and self.alquiler.fecha_inicio and self.alquiler.fecha_fin:
            self.dias_a_cobrar = (
                self.alquiler.fecha_fin - self.alquiler.fecha_inicio).days + 1

        if not self.dias_a_cobrar:
            self.dias_a_cobrar = 1

        # En este nuevo modelo el precio_dia ya incluye IVA
        base_con_iva = Decimal(self.dias_a_cobrar) * Decimal(self.precio_dia) * Decimal(
            self.cantidad) if self.cantidad else Decimal(self.dias_a_cobrar) * Decimal(self.precio_dia) * 1
        descuento = base_con_iva * \
            (Decimal(self.descuento_porcentaje) / Decimal('100'))
        total = base_con_iva - descuento

        # Separar valor del IVA incluido en el precio
        if self.producto.iva_porcentaje:
            base_sin_iva = total * \
                (1 - (self.producto.iva_porcentaje / Decimal('100')))
            self.valor_iva = total - base_sin_iva
        else:
            base_sin_iva = total
            self.valor_iva = 0

        self.valor_item = total
        self.subtotal_item = self.valor_item - self.valor_iva

        try:
            precio_dia = PrecioProducto.objects.get(
                producto=self.producto).valor
        except:
            precio_dia = 0
        finally:
            self.precio_dia = precio_dia

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto} ({self.dias_a_cobrar} días a {self.precio_dia} c/u)"

    @property
    def subtotal_sin_iva(self):
        base_con_iva = Decimal(self.dias_a_cobrar) * \
            Decimal(self.precio_dia) * Decimal(self.cantidad)
        if self.valor_iva > 0:
            return (base_con_iva - self.valor_iva)
        return base_con_iva

    @property
    def valor_descuento(self):
        base = self.cantidad * self.dias_a_cobrar * self.precio_dia
        return base * (self.descuento_porcentaje / Decimal('100'))
    
    @property
    def total_abonado(self):
        return sum(a.valor for a in self.abonos.all())

    @property
    def saldo_pendiente(self):
        return max(self.total_con_descuento - self.total_abonado, 0)

    @property
    def puede_liquidarse(self):
        return self.estado != 'liquidado' and self.saldo_pendiente == 0

    def liquidar(self, usuario, observaciones=""):
        if not self.puede_liquidarse:
            raise ValueError("No se puede liquidar: saldo pendiente o ya está liquidado.")

        self.estado = 'liquidado'
        self.save(update_fields=['estado'])

        LiquidacionAlquiler.objects.create(
            alquiler=self,
            total_liquidado=self.total_abonado,
            observaciones=observaciones,
            liquidado_por=usuario
        )
class EventoAlquiler(models.Model):
    TIPOS = [
        ('estado', 'Cambio de estado'),
        ('salida', 'Entrega de productos'),
        ('devolucion', 'Devolución'),
        ('nota', 'Nota interna'),
    ]

    alquiler = models.ForeignKey(
        'Alquiler', on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField(blank=True)
    # Solo si aplica (como abono)
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # Para registrar estado si tipo = estado
    estado_asociado = models.CharField(max_length=20, blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

class AbonoAlquiler(models.Model):
    alquiler = models.ForeignKey('Alquiler', on_delete=models.CASCADE, related_name='abonos')
    fecha = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, blank=True)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Abono ${self.valor} - Alquiler #{self.alquiler.id}"

class LiquidacionAlquiler(models.Model):
    alquiler = models.OneToOneField('Alquiler', on_delete=models.CASCADE, related_name='liquidacion')
    fecha = models.DateTimeField(auto_now_add=True)
    total_liquidado = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True)
    liquidado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Liquidación Alquiler #{self.alquiler.id} - ${self.total_liquidado}"
