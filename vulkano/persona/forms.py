from django import forms
from .models import Persona

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellidos', 'tipo_documento', 'telefono', 'correo', 'direccion']
        widgets = {
             'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre completo'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre completo'
            }),
            'tipo_documento': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Teléfono'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Correo electrónico'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded resize-y focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Dirección',
                'rows': 2
            }),
        }
