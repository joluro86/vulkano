from django import forms
from producto.models import PrecioProducto

class PrecioProductoForm(forms.ModelForm):
    class Meta:
        model = PrecioProducto
        fields = ['producto', 'valor']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'w-full rounded border-gray-300 focus:border-[var(--primary-color)] focus:ring focus:ring-[var(--primary-color)] focus:ring-opacity-50'
            }),
            'valor': forms.TextInput(attrs={
                'placeholder': 'Ej: 20000',
                'class': 'w-full rounded border-gray-300 focus:border-[var(--primary-color)] focus:ring focus:ring-[var(--primary-color)] focus:ring-opacity-50'
            }),
        }
        labels = {
            'producto': 'Producto',
            'valor': 'Valor',
        }
