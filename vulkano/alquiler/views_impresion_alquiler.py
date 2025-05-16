from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from alquiler.models import Alquiler
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def imprimir_alquiler(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk, usuario__sucursal=request.user.sucursal)
    template = get_template('alquiler_pdf.html')

    context = {
        'alquiler': alquiler,
        'empresa': request.user.empresa,
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="alquiler_{alquiler.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response
