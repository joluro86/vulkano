from django.contrib import admin

# admin.py
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export.resources import ModelResource
from .models import Cliente

class ClienteResource(ModelResource):
    class Meta:
        model = Cliente
        import_id_fields = ['documento']
        fields = ['documento', 'nombre', 'apellidos', 'tipo_documento', 'telefono', 'correo', 'direccion', 'empresa', 'estado']

class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource
    list_display = ['nombre', 'documento', 'empresa', 'estado']
    search_fields = ['nombre', 'documento']

admin.site.register(Cliente, ClienteAdmin)

