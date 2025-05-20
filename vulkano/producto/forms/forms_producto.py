from django import forms
from producto.models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ['created_at', 'updated_at', 'creado_por', 'modificado_por', 'empresa', 'sucursal']
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
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'empresa'):
            self.fields['categoria'].queryset = user.empresa.categorias.all()
            self.fields['proveedor'].queryset = user.empresa.proveedores.all()
