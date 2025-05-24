from producto.models import Empresa
from django import forms
from empresa.models import Empresa, Sucursal


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nombre', 'nit', 'direccion', 'telefono',
            'ciudad', 'departamento', 'estado', 'logo',
        ]
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
            'ciudad': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Ciudad'
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Departamento'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
            }),
            'logo': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 p-2 rounded bg-white'}),
        }


class EmpresaEditForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'nit', 'direccion',
                  'telefono', 'ciudad', 'departamento', 'estado', 'logo']
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
            'logo': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 p-2 rounded bg-white'}),
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['empresa', 'nombre', 'ciudad', 'direccion',
                  'departamento', 'telefono', 'estado']
        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre de la sucursal'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Ciudad'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Dirección'
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Departamento'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Teléfono'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
            }),
        }


class SucursalEditForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['empresa', 'nombre', 'ciudad', 'direccion',
                  'departamento', 'telefono', 'estado']
        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Nombre de la sucursal'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Ciudad'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Dirección'
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Departamento'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
                'placeholder': 'Teléfono'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
            }),
        }
