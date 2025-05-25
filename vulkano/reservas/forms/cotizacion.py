from django import forms
from reservas.models import Reserva
from producto.models import Producto
from cliente.models import Cliente

class CotizacionForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        label="Cliente",
        widget=forms.Select(attrs={"class": "w-full border rounded px-3 py-2"})
    )
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(),
        label="Producto",
        widget=forms.Select(attrs={"class": "w-full border rounded px-3 py-2"})
    )
    fecha_inicio = forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={"type": "date", "class": "w-full border rounded px-3 py-2"})
    )
    fecha_fin = forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={"type": "date", "class": "w-full border rounded px-3 py-2"})
    )

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=empresa)
            self.fields['producto'].queryset = Producto.objects.filter(empresa=empresa, estado='activo')