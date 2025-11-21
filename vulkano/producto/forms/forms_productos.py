# producto/forms/forms_productos.py
from django import forms
from producto.models import Producto

TAILWIND_SELECT = "w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"

class BusquedaProductoForm(forms.Form):
    marca = forms.ChoiceField(
        choices=[("", "Todas")],
        required=False,
        label="Marca",
        widget=forms.Select(attrs={"class": TAILWIND_SELECT})
    )
    estado = forms.ChoiceField(
        choices=[("", "Todos")] + list(Producto.ESTADOS),
        required=False,
        label="Estado",
        widget=forms.Select(attrs={"class": TAILWIND_SELECT})
    )
    ubicacion_actual = forms.ChoiceField(
        choices=[("", "Todas")],
        required=False,
        label="Municipio",
        widget=forms.Select(attrs={"class": TAILWIND_SELECT})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        marcas = (Producto.objects.exclude(marca__isnull=True)
                                  .exclude(marca__exact="")
                                  .values_list("marca", flat=True)
                                  .distinct().order_by("marca"))
        ubicaciones = (Producto.objects.exclude(ubicacion_actual__isnull=True)
                                       .exclude(ubicacion_actual__exact="")
                                       .values_list("ubicacion_actual", flat=True)
                                       .distinct().order_by("ubicacion_actual"))
        self.fields["marca"].choices += [(m, m) for m in marcas]
        self.fields["ubicacion_actual"].choices += [(u, u) for u in ubicaciones]
