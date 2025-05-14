from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
            'placeholder': 'Nombre de usuario'
        })
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)]',
            'placeholder': 'Contraseña'
        })
    )
class UsuarioCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Repite la contraseña'
        })
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'telefono', 'empresa', 'sucursal',
            'estado', 'foto_perfil'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'empresa': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'sucursal': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'estado': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 p-2 rounded bg-white'}),
        }

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'email',
            'telefono', 'empresa', 'sucursal',
            'estado', 'foto_perfil'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'empresa': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'sucursal': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'estado': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 p-2 rounded bg-white'}),
        }
