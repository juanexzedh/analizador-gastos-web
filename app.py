from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import os
import pandas as pd
from servicios.analizador import (lector_archivo, calcular_total, calcular_total_ingresos, calcular_por_categoria, verificar_presupuesto, calcular_semaforo)
from servicios.database import inicializar_db, guardar_gastos, obtener_resumen_periodos, obtener_periodos_disponibles, obtener_gastos
from servicios.categorizer import categorizar
import calendar
from datetime import datetime
from servicios.predictor import proyectar_cierre, predecir_proximo_mes

app = Flask(__name__)
app.secret_key = "clave_secreta_para_mensajes_flash" # Necesario para mostrar alertas amigables de error

@app.template_filter('cop')
def formato_cop(valor):
    try:
        # Formatea con comas como separador de miles, y luego las reemplaza por puntos
        numero_formateado = f"{int(valor):,}".replace(',', '.')
        return f"{numero_formateado} COP"
    except (ValueError, TypeError):
        return valor # Si falla, devuelve el valor original

# Inicializar la base de datos al arrancar la app
inicializar_db()

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route('/instructivo')
def instructivo():
    return render_template('instructivo.html')


@app.route("/analizar", methods=["POST"])
def analizar():
    archivo = request.files.get("archivo")
    presupuesto = request.form.get("presupuesto", 0)
    periodo = request.form.get("periodo") # Se obtiene el periodo del formulario

    # Validacionesdel formulario
    if not archivo or archivo.filename == '':
        flash("Por favor, sube un archivo válido.")
        return redirect(url_for('inicio'))
        
    if not periodo:
        flash("Por favor, selecciona un periodo (Mes/Año).")
        return redirect(url_for('inicio'))

    # Guardar archivo temporalmente para procesarlo
    os.makedirs('uploads', exist_ok=True)
    ruta_archivo = os.path.join('uploads', archivo.filename)
    archivo.save(ruta_archivo)

    try:
        # Leer el archivo
        df = lector_archivo(ruta_archivo)
        
        # Categorizacion Automatica
        for index, row in df.iterrows():
            if row['tipo'] == 'gasto':
                # Si es nulo o vacio en el archivo
                if pd.isna(row['categoria']) or str(row['categoria']).strip() == '':
                    df.at[index, 'categoria'] = categorizar(row['descripcion'])
            else:
                df.at[index, 'categoria'] = 'Ingreso'

        # Guardar en SQLite
        lista_movimientos = df.to_dict(orient='records')
        guardar_gastos(lista_movimientos, periodo)

        # Calculos para el Dashboard
        total_gastos = calcular_total(df)
        total_ingresos = calcular_total_ingresos(df)
        ahorrado = total_ingresos - total_gastos
        totalxcategoria = calcular_por_categoria(df)
        supero_presupuesto = verificar_presupuesto(total_gastos, float(presupuesto))
        semaforo = calcular_semaforo(total_gastos, total_ingresos)

        # Para calcular el dia con mas gasto
        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce')
        df['Dia_Semana'] = df['fecha'].dt.day_name()
        dias_espanol = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
        }
        df['Dia_Semana'] = df['Dia_Semana'].map(dias_espanol)

        gastos = df[df['tipo'] == 'gasto']
        gastos_por_dia = gastos.groupby('Dia_Semana')['monto'].sum()
        dia_pico = gastos_por_dia.idxmax()
        monto_pico = gastos_por_dia.max()

    except Exception as e:
        flash(f"Error procesando el archivo: {str(e)}")
        return redirect(url_for('inicio'))
    finally:
        # Limpieza preventiva del archivo temporal subido
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

    # Renderizar la pagina de resultados unificada
    return render_template(
        "resultado.html",
        periodo=periodo,
        total_gastos=total_gastos,
        total_ingresos=total_ingresos,
        totalxcategoria=totalxcategoria,
        supero_presupuesto=supero_presupuesto,
        semaforo=semaforo,
        dia_pico=dia_pico,
        monto_pico=monto_pico,
        ahorrado=ahorrado 
    )


@app.route("/historial")
def historial():
    # Cargar los datos base de la pagina
    datos_historial = obtener_resumen_periodos()
    periodos_simples = obtener_periodos_disponibles() 
    
    # Capturar posibles parámetros de comparacion en la URL
    mes_a = request.args.get('mes_a')
    mes_b = request.args.get('mes_b')
    tabla_comparativa = None  # Por defecto no hay tabla

    # Si el usuario selecciono dos meses, hacemos el calculo de Pandas
    if mes_a and mes_b:
        datos_a = obtener_gastos(mes_a)
        datos_b = obtener_gastos(mes_b)
        
        df_a = pd.DataFrame(datos_a)
        df_b = pd.DataFrame(datos_b)
        
        if not df_a.empty:
            gastos_a = df_a[df_a['tipo'] == 'gasto'].groupby('categoria')['monto'].sum().reset_index()
        else:
            gastos_a = pd.DataFrame(columns=['categoria', 'monto'])
            
        if not df_b.empty:
            gastos_b = df_b[df_b['tipo'] == 'gasto'].groupby('categoria')['monto'].sum().reset_index()
        else:
            gastos_b = pd.DataFrame(columns=['categoria', 'monto'])
            
        df_comparativo = pd.merge(gastos_a, gastos_b, on='categoria', how='outer', suffixes=('_a', '_b')).fillna(0)
        df_comparativo['diferencia_pesos'] = df_comparativo['monto_b'] - df_comparativo['monto_a']
        df_comparativo['diferencia_porcentaje'] = df_comparativo.apply(
            lambda row: (row['diferencia_pesos'] / row['monto_a'] * 100) if row['monto_a'] > 0 else 100.0, 
            axis=1
        )
        
        tabla_comparativa = df_comparativo.to_dict(orient='records')

    # Enviar todo al mismo HTML
    return render_template(
        'historial.html', 
        historial=datos_historial, 
        periodos=periodos_simples,
        tabla=tabla_comparativa,#puede ser none
        mes_a=mes_a,
        mes_b=mes_b
    )


@app.route('/descargar-plantilla')
def descargar_plantilla():
    directorio_assets = os.path.join(app.root_path, 'static', 'assets')    
    # as_attachment=True fuerza al navegador a descargarlo en lugar de intentar abrirlo
    return send_from_directory(directorio_assets, 'plantilla.xlsx', as_attachment=True, download_name='plantilla.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route("/descargar-pdf/<periodo>")
def descargar_pdf(periodo):
    # Por ahora, una confirmación simple para verificar que el enlace funciona
    return f"Generando reporte PDF para el periodo: {periodo}. (Lógica en construcción)"

if __name__ == "__main__":
    app.run(debug=True)