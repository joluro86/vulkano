# inventario/forms.py

from django import forms
from inventario.models import MovimientoInventario, MovimientoItem

from django import forms
from inventario.models import MovimientoInventario
from cliente.models import Cliente
from producto.models import Proveedor

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['tipo', 'observacion', 'proveedor', 'cliente']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ocultar proveedor y cliente por defecto
        self.fields['proveedor'].required = False
        self.fields['cliente'].required = False

        # Ocultar campos visualmente según tipo
        if self.instance:
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

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return cantidad
