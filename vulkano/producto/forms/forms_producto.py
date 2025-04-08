from django import forms
from producto.models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'codigo_interno', 'estado',
            'ubicacion_actual', 'fecha_ingreso', 'marca', 'modelo',
            'serial', 'stock', 'imagen', 'empresa', 'sucursal',
            'categoria', 'proveedor'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded resize-y focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Descripción del producto',
                'rows': 3
            }),
            'codigo_interno': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Código interno'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]'
            }),
            'ubicacion_actual': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Ubicación actual'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]'
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
            'stock': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'min': 0
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray-300 p-2 rounded bg-white'
            }),
            'empresa': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'sucursal': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'proveedor': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
        }
