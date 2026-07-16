from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import os
import pandas as pd
from servicios.analizador import (lector_archivo, calcular_total, calcular_total_ingresos, calcular_por_categoria, verificar_presupuesto, calcular_semaforo)
from servicios.database import inicializar_db, guardar_gastos, obtener_periodos_disponibles
from servicios.categorizer import categorizar

app = Flask(__name__)
app.secret_key = "clave_secreta_para_mensajes_flash" # Necesario para mostrar alertas amigables de error

# Inicializar la base de datos al arrancar la app
inicializar_db()

@app.route("/")
def inicio():
    return render_template("index.html")

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
        totalxcategoria = calcular_por_categoria(df)
        supero_presupuesto = verificar_presupuesto(total_gastos, float(presupuesto))
        semaforo = calcular_semaforo(total_gastos, total_ingresos)

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
        semaforo=semaforo
    )

@app.route('/descargar-plantilla')
def descargar_plantilla():
    directorio_assets = os.path.join(app.root_path, 'static', 'assets')    
    # as_attachment=True fuerza al navegador a descargarlo en lugar de intentar abrirlo
    return send_from_directory(directorio_assets, 'plantilla.xlsx', as_attachment=True, download_name='plantilla.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app.run(debug=True)