from django import forms
from producto.models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'empresa']
        exclude = ['empresa']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre de la Categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Descripción de la Categoría',
                'rows': 3,
            }),
        }
