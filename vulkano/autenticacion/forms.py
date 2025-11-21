from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario, Rol
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from persona.models import Persona
from cliente.models import Cliente


def generar_username_auto(nombre, apellidos):
    nombre_partes = nombre.strip().split()
    apellido_partes = apellidos.strip().split()

    nombre_base = nombre_partes[0].lower() if nombre_partes else ''
    primer_apellido = apellido_partes[0].lower() if apellido_partes else ''
    inicial_segundo_apellido = apellido_partes[1][0].lower() if len(apellido_partes) > 1 else ''

    base = f"{nombre_base[0]}{primer_apellido}{inicial_segundo_apellido}"

    Usuario = get_user_model()
    username = base

    i = 1
    while Usuario.objects.filter(username=username).exists():
        # Agrega más letras del primer nombre, luego del segundo nombre si hay
        if i < len(nombre_base):
            username = f"{nombre_base[:i+1]}{primer_apellido}{inicial_segundo_apellido}"
        elif len(nombre_partes) > 1 and i - len(nombre_base) < len(nombre_partes[1]):
            segunda_parte = nombre_partes[1]
            extra = segunda_parte[:i - len(nombre_base) + 1]
            username = f"{nombre_base}{extra}{primer_apellido}{inicial_segundo_apellido}"
        else:
            username = f"{base}x"
        i += 1

    return username


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
            'telefono', 'empresa', 'sucursal', 'rol',
            'estado', 'foto_perfil'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'id': 'id_username'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'id': 'id_first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'id': 'id_last_name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'empresa': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'sucursal': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'rol': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'estado': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 p-2 rounded bg-white'}),
        }

    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        empresa = cleaned_data.get('empresa')

        if username and empresa:
            if Usuario.objects.filter(username=username, empresa=empresa).exists():
                raise ValidationError({
                    'username': "Ya existe un usuario con este nombre en esta empresa."
                })

        return cleaned_data



class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'telefono', 'empresa', 'sucursal', 'rol',
            'estado', 'foto_perfil'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded bg-gray-100',
                'readonly': 'readonly',
                 'id': 'id_username'
            }),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'id': 'id_first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'id': 'id_last_name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'empresa': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'sucursal': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'rol': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'estado': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded bg-white'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 p-2 rounded bg-white'}),
        }

    def clean_username(self):
        return self.instance.username

class ClienteRegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Apellidos'
        })
    )
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Nombre de usuario'
        })
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Correo electrónico'
        })
    )

    tipo_documento = forms.ChoiceField(
        label="Tipo de documento",
        choices=Persona.TIPO_DOCUMENTO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded bg-white',
        })
    )
    documento = forms.CharField(
        label="Número de documento",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Número de documento'
        })
    )
    telefono = forms.CharField(
        label="Teléfono",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded',
            'placeholder': 'Teléfono de contacto'
        })
    )

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
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        # Configuración de usuario cliente
        user.is_staff = False
        user.is_superuser = False
        user.estado = "activo"

        telefono = self.cleaned_data.get('telefono')
        if telefono:
            user.telefono = telefono

        # Rol por defecto: cliente
        rol_cliente, _ = Rol.objects.get_or_create(
            nombre="cliente",
            defaults={'descripcion': 'This is a current client'}
        )
        user.rol = rol_cliente

        if commit:
            user.save()

            # Grupo por defecto: cliente
            group, _ = Group.objects.get_or_create(name="cliente")
            user.groups.add(group)

            # Datos del formulario
            numero_doc = self.cleaned_data.get('documento')
            tipo_doc = self.cleaned_data.get('tipo_documento')
            empresa = getattr(user, 'empresa', None)  # puede ser None

            # 👇 Aquí se crea un Cliente (NO Persona)
            Cliente.objects.create(
                # Campos heredados de Persona:
                usuario=user,
                nombre=user.first_name or user.username,
                apellidos=user.last_name or "",
                tipo_documento=tipo_doc,
                telefono=telefono,
                correo=user.email,
                direccion=None,

                # Campos propios de Cliente:
                documento=numero_doc,
                empresa=empresa,
                estado=True,
            )

        return user
