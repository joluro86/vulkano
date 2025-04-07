from django.db import models
from empresa.models import Empresa

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(blank=True, null=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias', default=1)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        unique_together = ('nombre', 'empresa')
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
class Proveedor(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=50, unique=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="activo")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='proveedores', default=1)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    ESTADOS = [
        ("disponible", "Disponible"),
        ("alquilado", "Alquilado"),
        ("mantenimiento", "En mantenimiento"),
        ("inactivo", "Inactivo"),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    codigo_interno = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="disponible")
    ubicacion_actual = models.CharField(max_length=100)
    precio_alquiler_dia = models.DecimalField(max_digits=10, decimal_places=2)
    precio_alquiler_semana = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_ingreso = models.DateField()
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    serial = models.CharField(max_length=100, blank=True, null=True)
    stock = models.PositiveIntegerField(default=1)
    imagen = models.ImageField(upload_to="productos/", null=True, blank=True)
    activo = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos', default=1)    

    def __str__(self):
        return f"{self.nombre} ({self.codigo_interno})"

class DetalleProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='detalles', on_delete=models.CASCADE)
    atributo = models.CharField(max_length=100)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.atributo}: {self.valor}"

