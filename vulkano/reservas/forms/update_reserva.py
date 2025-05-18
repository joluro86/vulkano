# reservas/forms/update_reserva.py
from django import forms
from reservas.models import Reserva

class UpdateReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'producto', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(
                format='%Y-%m-%d',              #formato ISO
                attrs={'type': 'date'}
            ),
            'fecha_fin': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }

    # con esto el widget recibe el valor de la instancia en formato ISO
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['fecha_inicio'].initial = self.instance.fecha_inicio.strftime('%Y-%m-%d')
            self.fields['fecha_fin'].initial = self.instance.fecha_fin.strftime('%Y-%m-%d')
