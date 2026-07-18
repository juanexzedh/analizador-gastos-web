from sklearn.linear_model import LinearRegression

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