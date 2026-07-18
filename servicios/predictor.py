from sklearn.linear_model import LinearRegression
import numpy as np

def proyectar_cierre(df_mes_actual, dia_actual, dias_en_mes):
    # Verificar que el dataframe no este vacio
    if df_mes_actual.empty:
        return 0

    gastos = df_mes_actual[df_mes_actual['tipo'] == 'gasto']['monto'].sum()
    if dia_actual <= 0:
        return 0
    
    promedio_diario = gastos / dia_actual
    proyeccion_fin_de_mes = promedio_diario * dias_en_mes
    
    return proyeccion_fin_de_mes

def predecir_proximo_mes(historial):
    # Verifica si hay menos de 3 meses
    meses_totales = len(historial)
    if meses_totales < 3:
        meses_faltantes = 3 - meses_totales
        return {
            "estado": "error", 
            "mensaje": f"Se necesitan 3 meses de historial. Faltan {meses_faltantes}."
        }

    # Invertir el historial para que quede de ma antiguo a más reciente
    historial_cronologico = list(reversed(historial))
    # Variable y (Gastos)
    y = [mes['gastos'] for mes in historial_cronologico]
    #Variable X, Scikit-learn pide que X sea una matriz 2D (ej: [[1], [2], [3]])
    X = [[i] for i in range(1, len(historial_cronologico) + 1)]
    
    #Entrenar modelo y predecir el mes siguiente
    modelo = LinearRegression()
    modelo.fit(X, y)
    # El mes a predecir es el total actual + 1
    mes_futuro = len(historial_cronologico) + 1
    prediccion = modelo.predict([[mes_futuro]])
    
    return {
        "estado": "exito", 
        "prediccion": prediccion[0]
    }