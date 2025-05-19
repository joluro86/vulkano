from django import forms
from descuento.models import Descuento

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        exclude = ['empresa', 'created_at', 'updated_at', 'creado_por', 'modificado_por']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Nombre del descuento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded resize-y',
                'placeholder': 'Descripción (opcional)',
                'rows': 2
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'porcentaje': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Ej. 10 para 10%',
                'min': 0,
                'max': 100,
                'step': 0.01
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-[var(--primary-color)] focus:ring-[var(--primary-color)] border-gray-300 rounded'
            }),
        }
