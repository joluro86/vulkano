# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Empresa
from empresa.forms.empresa_forms import EmpresaForm
from empresa.logic.empresa_logic import create_empresa

class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'crear_empresa.html'
    success_url = reverse_lazy('empresa_list')

    def form_valid(self, form):
        # Aquí llamamos la creación de la empresa a nuestro logic
        create_empresa(form)
        return super().form_valid(form)

class EmpresaListView(ListView):
    model = Empresa
    template_name = "empresa_list.html"

