from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from alquiler.models import AbonoAlquiler, LiquidacionAlquiler, AlquilerItem
from persona.models import Persona
from inventario.models import InventarioSucursal


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

    
    mas_alquilado = productos.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido').first()or {}

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

    return render(request, 'estadisticos_producto.html', {
        'top5_alquilados': top5_alquilados,
        'menos_inventario': menos_inventario,
        'grafico': grafico_base64,  
    })

