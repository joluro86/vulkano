from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol
from persona.models import Persona

class PersonaInline(admin.StackedInline):
    model = Persona
    can_delete = False
    extra = 0

@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active','rol','get_groups')
    list_filter = ('is_staff', 'is_active', 'empresa', 'sucursal','rol', 'estado')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Información personal', {
            'fields': ('first_name', 'last_name', 'email', 'telefono', 'foto_perfil')
        }),
        ('Empresa y rol', {
            'fields': ('empresa', 'sucursal', 'rol', 'estado')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')

    def get_groups(self, obj):
        # Devuelve los nombres de los grupos separados por coma
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = "Grupos"


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)