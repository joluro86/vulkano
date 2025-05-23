from django import forms
from alquiler.models import Alquiler, AlquilerItem
from producto.models import Producto
from django import forms
from cliente.models import Cliente
class AlquilerCrearForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = []  # No se muestra ningún campo
class AlquilerEditarForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['cliente', 'fecha_inicio', 'fecha_fin', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]'
            }, format='%Y-%m-%d'),  # 👈 Asegura el formato
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]'
            }, format='%Y-%m-%d'),  # 👈 Asegura el formato
            'observaciones': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded resize-y focus:ring-2 focus:ring-[var(--primary-color)]',
                'rows': 2,
                'placeholder': 'Observaciones del alquiler...'
            }),
        }

    def __init__(self, *args, sucursal=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sucursal:
            self.fields['cliente'].queryset = Cliente.objects.filter(
                empresa=sucursal.empresa,
                estado=True
            ).order_by('nombre')

        # 👇 Este bloque asegura que las fechas aparezcan correctamente en el form
        for campo in ['fecha_inicio', 'fecha_fin']:
            if self.instance and getattr(self.instance, campo):
                self.fields[campo].initial = getattr(self.instance, campo).strftime('%Y-%m-%d')

from django import forms
from alquiler.models import AlquilerItem
from producto.models import Producto

class AlquilerItemForm(forms.ModelForm):
    class Meta:
        model = AlquilerItem
        fields = ['dias_a_cobrar', 'cantidad',]
        widgets = {
            'dias_a_cobrar': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'min': 1,
                'placeholder': 'Opcional, se calcula si no se digita'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'min': 0,
                'step': 1,
                'placeholder': 'Digite la cantidad de producto a alquilar'
            }),
           }

    def __init__(self, *args, sucursal=None, **kwargs):
        super().__init__(*args, **kwargs)
        # No se usa producto como campo, pero podrías condicionar si vuelves a usar el campo en otros formularios
        if 'producto' in self.fields and sucursal:
            self.fields['producto'].queryset = Producto.objects.filter(sucursal=sucursal)

    def clean_dias_a_cobrar(self):
        dias = self.cleaned_data.get('dias_a_cobrar')
        if dias is not None and dias <= 0:
            raise forms.ValidationError("Debe ser al menos 1 día.")
        return dias

    def clean_precio_dia(self):
        precio = self.cleaned_data.get('precio_dia')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio
