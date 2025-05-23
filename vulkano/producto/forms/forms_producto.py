from django import forms
from producto.models import Producto, PrecioProducto


class ProductoForm(forms.ModelForm):

    precio = forms.DecimalField(
        label='Precio por día', max_digits=10, decimal_places=0)

    class Meta:
        model = Producto
        exclude = ['created_at', 'updated_at', 'creado_por',
                   'modificado_por', 'empresa', 'sucursal']
        fields = ['nombre', 'descripcion', 'codigo_interno', 'estado', 'iva_porcentaje',
                  'ubicacion_actual', 'modelo', 'marca', 'serial', 'precio', 'imagen', 'categoria', 'proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre del producto'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded resize-y focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Descripción del producto',
                'rows': 3
            }),
            'codigo_interno': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Código interno'
            }),

            'ubicacion_actual': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Ubicación actual'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Marca'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Modelo'
            }),
            'serial': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Serial'
            }),
            'precio': forms.TextInput(attrs={
                'placeholder': 'Ej: 20000',
                'class': 'w-full p-2 border border-gray-300 rounded'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray-300 p-2 rounded bg-white'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'proveedor': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'iva_porcentaje': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'min': 0,
                'step': 1,
                'placeholder': 'Ej. 19 para 19%',
            })


        }

    def save(self, commit=True):
        producto = super().save(commit)
        valor = self.cleaned_data.get('precio')

        PrecioProducto.objects.update_or_create(
        producto=producto,
                defaults={'valor': valor}
            )
        return producto

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            try:
                precio_obj = PrecioProducto.objects.get(producto=self.instance)
                self.fields['precio'].initial = int(precio_obj.valor)
            except PrecioProducto.DoesNotExist:
                self.fields['precio'].initial = 0

        if user and hasattr(user, 'empresa'):
            self.fields['categoria'].queryset = user.empresa.categorias.all()
            self.fields['proveedor'].queryset = user.empresa.proveedores.all()
            self.fields['precio'].widget.attrs.update({
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Ej: 20000'
            })
