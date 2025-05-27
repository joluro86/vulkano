from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'tipo_documento', 'documento', 'telefono', 'correo', 'direccion', 'estado']
        labels = {
            'estado': 'Activo'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Apellidos'
            }),
            'tipo_documento': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white'
            }),
            'documento': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded',
                'placeholder': 'Número de documento'
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
            'estado': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-[var(--primary-color)] focus:ring-[var(--primary-color)] border-gray-300 rounded'
            }),
        }
