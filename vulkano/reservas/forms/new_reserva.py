# reservas/forms.py
from django import forms
from reservas.models import Reserva
from producto.models import Producto
from cliente.models import Cliente


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'producto', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)  # <-- obtener empresa
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['producto'].queryset = Producto.objects.filter(estado='activo', empresa=empresa)
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=empresa)  # <-- filtrar clientes
        else:
            self.fields['producto'].queryset = Producto.objects.filter(estado='activo')
            self.fields['cliente'].queryset = Cliente.objects.all()  # <-- clientes sin filtro