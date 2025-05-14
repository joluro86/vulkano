from django import forms
from django.contrib.auth.forms import AuthenticationForm

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

