from django import forms
from alquiler.models import Alquiler, AlquilerItem
from producto.models import Producto

class AlquilerCrearForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = []  # No se muestra ningún campo

from django import forms
from alquiler.models import Alquiler

class AlquilerEditarForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['fecha_inicio', 'fecha_fin', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]'
                },
                format='%Y-%m-%d'  # 👈 Esto es lo importante
            ),
            'fecha_fin': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]'
                },
                format='%Y-%m-%d'  # 👈 Esto también
            ),
            'observaciones': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded resize-y focus:ring-2 focus:ring-[var(--primary-color)]',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegura que el valor inicial se pase en el formato adecuado
        for field in ['fecha_inicio', 'fecha_fin']:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%Y-%m-%d')


class AlquilerItemForm(forms.ModelForm):
    class Meta:
        model = AlquilerItem
        fields = ['producto', 'dias_a_cobrar', 'precio_dia']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'dias_a_cobrar': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Días a cobrar'
            }),
            'precio_dia': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Precio por día'
            }),
        }

    def __init__(self, *args, **kwargs):
        sucursal = kwargs.pop('sucursal', None)
        super().__init__(*args, **kwargs)
        if sucursal:
            self.fields['producto'].queryset = Producto.objects.filter(sucursal=sucursal)
