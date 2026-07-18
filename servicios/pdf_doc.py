from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
import pandas as pd

def generar_pdf(mes, anio, datos):
    output = BytesIO()
    doc = SimpleDocTemplate(output)
    estilos = getSampleStyleSheet()
    elementos = []

    #Encabezado
    titulo = Paragraph(f"Reporte Financiero - {mes}/{anio}", estilos['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 20))

    df = pd.DataFrame(datos)
    if df.empty:
        elementos.append(Paragraph("No hay registros para este periodo.", estilos['Normal']))
        doc.build(elementos)
        return output.getvalue()

    # Calculos principales
    ingresos = df[df['tipo'] == 'ingreso']['monto'].sum()
    gastos = df[df['tipo'] == 'gasto']['monto'].sum()
    balance = ingresos - gastos

    # Metricas principales
    elementos.append(Paragraph("Métricas Principales", estilos['Heading2']))
    datos_metricas = [
        ['Total Ingresos', 'Total Gastos', 'Balance'],
        [f"${ingresos:,.0f}", f"${gastos:,.0f}", f"${balance:,.0f}"]
    ]
    tabla_metricas = Table(datos_metricas, colWidths=[150, 150, 150])
    tabla_metricas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#343a40")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elementos.append(tabla_metricas)
    elementos.append(Spacer(1, 20))

    # Semaforo
    elementos.append(Paragraph("Estado Financiero (Semáforo)", estilos['Heading2']))
    if balance > 0:
        texto_semaforo = "<font color='green'>🟢 VERDE: ¡Buen trabajo! Gastaste menos de lo que ingresó.</font>"
    elif balance == 0:
        texto_semaforo = "<font color='orange'>🟡 AMARILLO: Cuidado. Quedaste exactamente en ceros.</font>"
    else:
        texto_semaforo = "<font color='red'>🔴 ROJO: Alerta. Tus gastos superaron tus ingresos.</font>"
    
    elementos.append(Paragraph(texto_semaforo, estilos['Normal']))
    elementos.append(Spacer(1, 20))

    #Tabla de gastos por categoria
    elementos.append(Paragraph("Gastos por Categoría", estilos['Heading2']))
    df_gastos = df[df['tipo'] == 'gasto']
    gastos_cat = df_gastos.groupby('categoria')['monto'].sum().reset_index()
    
    datos_cat = [['Categoría', 'Total']]
    for _, row in gastos_cat.iterrows():
        datos_cat.append([row['categoria'], f"${row['monto']:,.0f}"])
        
    tabla_cat = Table(datos_cat, colWidths=[200, 150])
    tabla_cat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#17a2b8")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elementos.append(tabla_cat)
    elementos.append(Spacer(1, 20))

    # Top 5 mas altos
    elementos.append(Paragraph("Top 5 Gastos Más Altos", estilos['Heading2']))
    top_5 = df_gastos.nlargest(5, 'monto')
    
    datos_top = [['Descripción', 'Monto']]
    for _, row in top_5.iterrows():
        datos_top.append([row['descripcion'], f"${row['monto']:,.0f}"])
        
    tabla_top = Table(datos_top, colWidths=[300, 100])
    tabla_top.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#dc3545")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elementos.append(tabla_top)

    # Construir PDF
    doc.build(elementos)
    return output.getvalue()