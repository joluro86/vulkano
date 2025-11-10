from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from alquiler.models import AbonoAlquiler, LiquidacionAlquiler, AlquilerItem, Alquiler
from persona.models import Persona
from inventario.models import InventarioSucursal
from django.db.models import Avg, F, ExpressionWrapper, DurationField
from datetime import timedelta
from django.db.models import Count, Avg
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from matplotlib.ticker import MaxNLocator


import seaborn as sns
import matplotlib
matplotlib.use("Agg")  # Backend para entornos sin interfaz gráfica
import matplotlib.pyplot as plt
import pandas as pd
import io, base64
import matplotlib.ticker as ticker

@login_required
def informeGeneral(request):
    abonos = AbonoAlquiler.objects.all()
    liquidaciones = LiquidacionAlquiler.objects.all()
    productos = AlquilerItem.objects.all()
    total_personas = Persona.objects.count()
    total_abonos = abonos.aggregate(total=Sum('valor'))['total'] or 0
    total_liquidado = liquidaciones.aggregate(total=Sum('total_liquidado'))['total'] or 0

    
    mas_alquilado = productos.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido').first()

    if mas_alquilado:
        mas_alquilado = {
            'nombre': mas_alquilado['producto__nombre'],
            'total_vendido': int(mas_alquilado['total_vendido'])
        }
    else:
        mas_alquilado = None

    abonos_mes = (
        AbonoAlquiler.objects
        .annotate(mes=TruncMonth("fecha"))
        .values("mes")
        .annotate(total=Sum("valor"))
        .order_by("mes")
    )

    liquidaciones_mes = (
        LiquidacionAlquiler.objects
        .annotate(mes=TruncMonth("fecha"))
        .values("mes")
        .annotate(total=Sum("total_liquidado"))
        .order_by("mes")
    )

    # Convertir a DataFrames
    df_abonos = pd.DataFrame(list(abonos_mes))
    df_liq = pd.DataFrame(list(liquidaciones_mes))

    # Unir en un solo DataFrame
    df = pd.merge(df_abonos, df_liq, on="mes", how="outer", suffixes=("_abonos", "_liquidado"))
    df = df.fillna(0)  # por si algún mes tiene solo abonos o liquidaciones

    # Reestructurar al formato "largo" (long format)
    df_long = pd.melt(
        df,
        id_vars=["mes"],
        value_vars=["total_abonos", "total_liquidado"],
        var_name="tipo",
        value_name="valor"
    )

    df_long["mes"] = pd.to_datetime(df_long["mes"]).dt.strftime("%Y-%m")

    # ---- Gráfico con Seaborn ----
    sns.set_theme(style="whitegrid")
    g = sns.catplot(
        data=df_long, kind="bar",
        x="mes", y="valor", hue="tipo",
        errorbar=None, palette={"total_abonos": "green", "total_liquidado": "blue"}, alpha=.7, height=6
    )
    g.set_axis_labels("Mes", "Monto")
    g.legend.set_title("")

    ax = g.ax
    ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", "."))
    )

    plt.subplots_adjust(left=0.15)

    # Guardar gráfico como imagen en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    imagen_png = buffer.getvalue()
    buffer.close()
    grafico_base64 = base64.b64encode(imagen_png).decode("utf-8")
    plt.close()  # liberar memoria


    request.session['grafico_general'] = grafico_base64
    request.session['total_abonos_general'] = float(total_abonos)
    request.session['total_liquidado_general'] = float(total_liquidado)
    request.session['total_personas_general'] = total_personas
    request.session['mas_alquilado_general'] = mas_alquilado

    request.session.modified = True

    return render(request, 'estadisticos_general.html', {
        'total_abonos': total_abonos,
        'total_liquidado': total_liquidado,
        'mas_alquilado': mas_alquilado,
        'total_personas': total_personas,
        'grafico': grafico_base64,  # lo pasamos al template
    })

@login_required
def informeProducto(request):
    productos = AlquilerItem.objects.all()

    top5_alquilados = (
        productos
        .values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')[:5]
    )

    menos_inventario = (
        InventarioSucursal.objects
        .values('producto__nombre', 'sucursal__nombre', 'stock_actual')
        .order_by('stock_actual')[:5]
    )

    alquilados_mes = (
    AlquilerItem.objects
    .annotate(mes=TruncMonth("alquiler__created_at"))   
    .values("mes", "producto__nombre")
    .annotate(total=Sum("cantidad"))
    .order_by("mes")
    )

    # Convertir a DataFrame
    df = pd.DataFrame(list(alquilados_mes))

    
    if not df.empty:
        df["mes"] = pd.to_datetime(df["mes"]).dt.strftime("%Y-%m")

    
        pivot_df = df.pivot_table(
            index="mes",
            columns="producto__nombre",
            values="total",
            aggfunc="sum",
            fill_value=0
        )

        # grafico apilado
        fig, ax = plt.subplots(figsize=(12, 6))

        pivot_df.plot(
            kind="bar",
            stacked=True,
            ax=ax,
            alpha=0.8,
            colormap="tab20"  
        )

        ax.set_ylabel("Cantidad Alquilada")
        ax.set_xlabel("Mes")
        ax.set_title("Productos alquilados por mes (apilado)")
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", "."))
        )

        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Producto", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()

        # Guardar gráfico como imagen en memoria
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer.close()
        grafico_base64 = base64.b64encode(imagen_png).decode("utf-8")
        plt.close()
    else:
        grafico_base64 = None

    request.session['top5_alquilados'] = list(top5_alquilados)
    request.session['menos_inventario'] = list(menos_inventario)
    request.session['grafico_producto'] = grafico_base64  

    request.session.modified = True  

    return render(request, 'estadisticos_producto.html', {
        'top5_alquilados': top5_alquilados,
        'menos_inventario': menos_inventario,
        'grafico': grafico_base64,  
    })


@login_required
def informeClientes(request):
    total_personas = Persona.objects.count()
    total_alquileres = Alquiler.objects.count()
    total_productos = AlquilerItem.objects.aggregate(total=Sum('cantidad'))['total'] or 0
  
    # Unir LiquidacionAlquiler con Alquiler
    liquidaciones = LiquidacionAlquiler.objects.select_related('alquiler').annotate(
        duracion=ExpressionWrapper(
            F('fecha') - F('alquiler__created_at'),
            output_field=DurationField()
        )
    )

    # Calcular promedio
    promedio_duracion = liquidaciones.aggregate(promedio=Avg('duracion'))['promedio']

    # Convertir a días (opcional)
    promedio_dias = None
    if promedio_duracion:
        promedio_dias = promedio_duracion.total_seconds() / 86400  # segundos → días

     
    alquileres_con_conteo = (
        Alquiler.objects.annotate(num_productos=Count('items__producto', distinct=True))
    )

    
    promedio_productos_por_alquiler = (
        alquileres_con_conteo.aggregate(promedio=Avg('num_productos'))['promedio'] or 0
    )

    # Agrupar por ubicación (ajusta el campo según tu modelo)
    personas_por_ubicacion = (
        Persona.objects
        .values('departamento')  # o 'ubicacion' si no usas FK
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Convertir a DataFrame para graficar
    df = pd.DataFrame(list(personas_por_ubicacion))

    if not df.empty and 'departamento' in df.columns:
        df = df.rename(columns={'departamento': 'Departamento', 'total': 'Cantidad'})

        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(
            kind='bar',
            x='Departamento',
            y='Cantidad',
            ax=ax,
            color='skyblue',
            legend=False
        )

        
        ax.set_xlabel("Departamento")
        ax.set_ylabel("Cantidad de personas")
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", "."))
        )
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

       
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer.close()
        grafico_base64 = base64.b64encode(imagen_png).decode('utf-8')
        plt.close()
    else:
        grafico_base64 = None

    request.session['total_personas_clientes'] = total_personas
    request.session['promedio_duracion_clientes'] = promedio_dias
    request.session['promedio_productos_por_alquiler_clientes'] = promedio_productos_por_alquiler
    request.session['grafico_clientes'] = grafico_base64    

    return render(request, 'estadisticos_clientes.html', {
        'total_personas': total_personas,
        'promedio_duracion': promedio_dias,
        'promedio_productos_por_alquiler': promedio_productos_por_alquiler,
        'grafico': grafico_base64,
    })

@login_required
def informeAlquiler(request):
    total_alquileres = Alquiler.objects.count()
    alquiler = Alquiler.objects.order_by('-total').first()
    if alquiler:
        datos = {
            'id': alquiler.id,
            'usuario': alquiler.usuario.username if alquiler.usuario else 'Sin usuario',
            'fecha_inicio': alquiler.fecha_inicio.strftime("%Y-%m-%d") if alquiler.fecha_inicio else '',
            'fecha_fin': alquiler.fecha_fin.strftime("%Y-%m-%d") if alquiler.fecha_fin else '',
            'estado': alquiler.estado,
            'total': float(alquiler.total) if alquiler.total is not None else 0,
        }
    else:
        datos = None

    # Obtener filtro desde GET (?filtro=mes)
    filtro = request.GET.get("filtro", "mes")  # valor por defecto: mes

    # Seleccionar truncado según filtro
    if filtro == "dia":
        trunc_func = TruncDay("fecha_inicio")
        formato_fecha = "%Y-%m-%d"
    elif filtro == "año":
        trunc_func = TruncYear("fecha_inicio")
        formato_fecha = "%Y"
    else:
        trunc_func = TruncMonth("fecha_inicio")
        formato_fecha = "%Y-%m"

    # Agrupar alquileres según el filtro
    alquileres_por_fecha = (
        Alquiler.objects
        .annotate(periodo=trunc_func)
        .values("periodo")
        .annotate(cantidad=Count("id"))
        .order_by("periodo")
    )

    # Convertir a DataFrame
    df = pd.DataFrame(list(alquileres_por_fecha))
    if not df.empty:
        df["periodo"] = pd.to_datetime(df["periodo"], errors="coerce")
        df = df.dropna(subset=["periodo"])  # elimina fechas no válidas
        df["periodo"] = df["periodo"].dt.strftime(formato_fecha)
        df["periodo"] = df["periodo"].astype(str)
        df["cantidad"] = df["cantidad"].astype(int)

        # Gráfico de línea
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df["periodo"], df["cantidad"])

        ax.minorticks_off()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))

        ax.set_xlabel("Fecha")
        ax.set_ylabel("Cantidad de alquileres")
        ax.set_title(f"Alquileres por {filtro.capitalize()}")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Guardar gráfico en memoria
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer.close()
        grafico_base64 = base64.b64encode(imagen_png).decode("utf-8")
        plt.close()
    else:
        grafico_base64 = None    
    
    request.session['grafico_estadistico'] = grafico_base64
    request.session['total_estadistico'] = total_alquileres
    request.session['filtro_estadistico'] = filtro
    request.session['alquiler_mayor'] = datos
    request.session.modified = True
    

    return render(request, 'estadisticos_alquiler.html', {
        'total_alquileres': total_alquileres,
        'alquiler': datos,
        'grafico': grafico_base64,
        'filtro': filtro,
    })

