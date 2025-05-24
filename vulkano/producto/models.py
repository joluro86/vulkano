from django.db import models
from empresa.models import Empresa, Sucursal

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

class ProductoManager(models.Manager):
    def por_empresa(self, empresa):
        return self.filter(empresa=empresa)
    
    def activos_por_empresa(self, empresa):
        return self.filter(empresa=empresa, estado='activo')
    
class Producto(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
        ("disponible", "Disponible"),
        ("no_disponible", "No disponible"),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    codigo_interno = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="activo")
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Porcentaje de IVA aplicado al producto")
    ubicacion_actual = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    serial = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.ImageField(upload_to="media/productos/", null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos', default=1)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='productos', default=1)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creado_por = models.CharField(max_length=100, blank=True, null=True)
    modificado_por = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        
        constraints = [
            models.UniqueConstraint(fields=['empresa', 'codigo_interno'], name='unique_codigo_por_empresa')
        ]

    def __str__(self):
        return f"{self.nombre} ({self.codigo_interno})"
    
    objects = ProductoManager()

class PrecioProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='precios', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.atributo}: {self.valor}"


