from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from alquiler.models import Alquiler
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from decimal import Decimal

@login_required
def imprimir_alquiler(request, pk):
    alquiler = get_object_or_404(Alquiler, pk=pk, usuario__sucursal=request.user.sucursal)

    # Cálculo manual para desglose
    subtotal = Decimal(0)
    iva_total = Decimal(0)
    total = Decimal(0)
    empresa = request.user.empresa

    for item in alquiler.items.select_related('producto'):
        total+= item.precio_dia*item.cantidad*item.dias_a_cobrar
        subtotal += item.subtotal_sin_iva
        iva_total += item.valor_iva


    template = get_template('alquiler_pdf.html')
    logo_url_absoluto = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None

    context = {
        'alquiler': alquiler,
        'empresa': empresa,
        'subtotal': subtotal,
        'iva_total': iva_total,
        'total': total,
        'logo_absoluto': logo_url_absoluto,
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="alquiler_{alquiler.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response
