from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from alquiler.models import Alquiler

@login_required
def imprimir_alquiler(request, pk):
    try:
        alquiler = Alquiler.objects.select_related('cliente', 'usuario').prefetch_related('items__producto').get(
            pk=pk, usuario__empresa=request.user.empresa)
    except Alquiler.DoesNotExist:
        messages.error(request, "El alquiler no existe o no tienes permiso para verlo.")
        return redirect('alquiler_list')

    subtotal = Decimal(0)
    iva_total = Decimal(0)
    total = Decimal(0)
    empresa = request.user.empresa

    for item in alquiler.items.select_related('producto'):
        total += item.precio_dia * item.cantidad * item.dias_a_cobrar
        subtotal += item.subtotal_sin_iva
        iva_total += item.valor_iva

    logo_url_absoluto = request.build_absolute_uri(empresa.logo.url) if empresa.logo else None

    context = {
        'alquiler': alquiler,
        'empresa': empresa,
        'subtotal': subtotal,
        'iva_total': iva_total,
        'total': total,
        'logo_absoluto': logo_url_absoluto,
    }

    template = get_template('alquiler_pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="alquiler_{alquiler.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response
