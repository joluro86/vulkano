# inventario/forms.py

from django import forms
from inventario.models import MovimientoInventario, MovimientoItem
from empresa.models import Sucursal
from producto.models import Producto

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['sucursal', 'tipo', 'observacion']
        widgets = {
            'sucursal': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded resize-y',
                'rows': 2,
                'placeholder': 'Opcional: motivo o detalles del movimiento'
            }),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['sucursal'].queryset = Sucursal.objects.filter(empresa=empresa)


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
