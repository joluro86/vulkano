from django import forms
from inventario.models import MovimientoInventario, MovimientoItem

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['tipo', 'observacion', 'proveedor', 'cliente']
        widgets = {
            'tipo': forms.Select(),
            'observacion': forms.Textarea(attrs={'rows': 3}),
            'proveedor': forms.Select(),
            'cliente': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Marcar proveedor y cliente como no obligatorios
        self.fields['proveedor'].required = False
        self.fields['cliente'].required = False

        # Mostrar u ocultar campos según el tipo de movimiento
        tipo = getattr(self.instance, 'tipo', None)
        if tipo == 'entrada':
            self.fields['proveedor'].widget.attrs['style'] = ''
            self.fields['cliente'].widget.attrs['style'] = 'display:none;'
        elif tipo == 'salida':
            self.fields['cliente'].widget.attrs['style'] = ''
            self.fields['proveedor'].widget.attrs['style'] = 'display:none;'
        else:
            self.fields['cliente'].widget.attrs['style'] = 'display:none;'
            self.fields['proveedor'].widget.attrs['style'] = 'display:none;'

        # Aplicar clases de Tailwind a todos los campos visibles
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.HiddenInput):
                if name == 'observacion':
                    field.widget.attrs.setdefault('class', 'w-full p-2 border border-gray-300 rounded resize-none')
                else:
                    field.widget.attrs.setdefault('class', 'w-full p-2 border border-gray-300 rounded')

class DetalleMovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoItem
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'min': 1,
                'placeholder': 'Cantidad del producto'
            }),
        }
        labels = {
            'cantidad': 'Cantidad',
        }
        help_texts = {
            'cantidad': 'Ingresa una cantidad mayor a 0.',
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return cantidad
