# services/empresa_service.py

def create_empresa(form):
    empresa = form.save()
    return empresa
