from django import forms
from empresa.models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'nit', 'direccion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre de la Empresa'
            }),
            'nit': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'NIT'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Dirección'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Teléfono'
            }),
        }


from django import forms
from producto.models import Empresa

class EmpresaEditForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'nit', 'direccion', 'telefono', 'ciudad', 'departamento', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre de la Empresa'
            }),
            'nit': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'NIT'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Dirección'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Teléfono'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Ciudad'
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Departamento'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:ring-2 focus:ring-[var(--primary-color)]',
            }),
        }
