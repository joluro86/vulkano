# reservas/forms/update_reserva.py
from django import forms
from reservas.models import Reserva
from producto.models import Producto
from cliente.models import Cliente


class UpdateReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'producto', 'precio', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'fecha_fin': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['fecha_inicio'].initial = self.instance.fecha_inicio.strftime('%Y-%m-%d')
            self.fields['fecha_fin'].initial = self.instance.fecha_fin.strftime('%Y-%m-%d')

            empresa = None
            if hasattr(self.instance, 'empresa'):
                empresa = self.instance.empresa
            elif self.instance.producto:
                empresa = self.instance.producto.empresa

            if empresa:
                self.fields['producto'].queryset = Producto.objects.filter(empresa=empresa, estado='activo')
                self.fields['cliente'].queryset = Cliente.objects.filter(empresa=empresa)  # <--- FILTRAR CLIENTES
            else:
                self.fields['producto'].queryset = Producto.objects.filter(estado='activo')
                self.fields['cliente'].queryset = Cliente.objects.all()  # Sin filtro si no hay empresa
        else:
            self.fields['producto'].queryset = Producto.objects.filter(estado='activo')
            self.fields['cliente'].queryset = Cliente.objects.all()
