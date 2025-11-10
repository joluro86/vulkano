from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

@login_required
def imprimir_estadistico(request):
    filtro = request.session.get("filtro_estadistico", "mes")
    grafico = request.session.get("grafico_estadistico")
    total = request.session.get("total_estadistico", 0)
    alquiler_mayor = request.session.get('alquiler_mayor', None)

    template = get_template('estadisticos_pdf.html')
    html = template.render({
        'grafico': grafico,
        'filtro': filtro,
        'total_alquileres': total,
        'alquiler_mayor': alquiler_mayor
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="estadistico_{filtro}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response

@login_required
def imprimir_general(request):
    total_abonos = request.session.get('total_abonos_general', 0)
    total_liquidado = request.session.get('total_liquidado_general', 0)
    total_personas = request.session.get('total_personas_general', 0)
    mas_alquilado = request.session.get('mas_alquilado_general', None)
    grafico = request.session.get('grafico_general', None)

    template = get_template("estadisticos_general_pdf.html")
    html = template.render({
        'total_abonos': total_abonos,
        'total_liquidado': total_liquidado,
        'total_personas': total_personas,
        'mas_alquilado': mas_alquilado,
        'grafico': grafico,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_general.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response

@login_required
def imprimir_producto(request):
    top5_alquilados = request.session.get('top5_alquilados', [])
    menos_inventario = request.session.get('menos_inventario', [])
    grafico = request.session.get('grafico_producto', None)

    template = get_template("estadisticos_producto_pdf.html")
    html = template.render({
        'top5_alquilados': top5_alquilados,
        'menos_inventario': menos_inventario,
        'grafico': grafico,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_producto.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response

@login_required
def generar_pdf_clientes(request):
    total_personas = request.session.get('total_personas_clientes', 0)
    promedio_dias = request.session.get('promedio_duracion_clientes', 0)
    promedio_productos_por_alquiler = request.session.get('promedio_productos_por_alquiler_clientes', 0)
    grafico_base64 = request.session.get('grafico_clientes', None)

    template = get_template('estadisticos_clientes_pdf.html')
    html = template.render({
        'total_personas': total_personas,
        'promedio_dias': promedio_dias,
        'promedio_productos_por_alquiler': round(promedio_productos_por_alquiler, 2),
        'grafico': grafico_base64,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="estadisticos_clientes.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response