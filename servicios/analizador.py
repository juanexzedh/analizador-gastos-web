import pandas as pd
import os

def lector_archivo(ruta_archivo):
    # Lee archivos CSV o Excel
    _, extension = os.path.splitext(ruta_archivo)
    if extension.lower() == '.xlsx':
        df = pd.read_excel(ruta_archivo)
    else:
        df = pd.read_csv(ruta_archivo)
        
    # Validar las columnas
    columnas_requeridas = ['fecha', 'descripcion', 'monto', 'tipo']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria: '{col}' en el archivo.")
            
    # Limpieza para evitar errores de formato
    df['tipo'] = df['tipo'].astype(str).str.strip().str.lower()
    df['descripcion'] = df['descripcion'].astype(str).str.strip()
    df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
    df['monto'] = df['monto'].fillna(0)
    
    # Si la columna 'categoria' no existe, se pone vacia para que el clasificador trabaje
    if 'categoria' not in df.columns:
        df['categoria'] = None
        
    return df

# Calcular el gasto total del DataFrame (solo filas tipo 'gasto')
def calcular_total(df):
    gastos = df[df['tipo'] == 'gasto']
    total = gastos["monto"].sum()
    return float(total)

# Calcular los ingresos totales (solo filas tipo 'ingreso')
def calcular_total_ingresos(df):
    ingresos = df[df['tipo'] == 'ingreso']
    total = ingresos["monto"].sum()
    return float(total)

# Calcular el gasto total por categoria 
def calcular_por_categoria(df):
    gastos = df[df['tipo'] == 'gasto']
    if gastos.empty:
        return {}
    categorias = gastos.groupby("categoria")
    totalcat = categorias["monto"].sum().to_dict()
    return totalcat

# Verificar si se supero el presupuesto o no
def verificar_presupuesto(total, presupuesto):
    return total > presupuesto

# Generar el estado del semáforo financiero
def calcular_semaforo(total_gastos, total_ingresos):
    if total_ingresos == 0:
        return "sin_ingresos"
        
    porcentaje = (total_gastos / total_ingresos) * 100
    
    if porcentaje <= 70:
        return "verde"     # Exito (Bootstrap: alert-success)
    elif porcentaje <= 90:
        return "amarillo"  # Cuidado (Bootstrap: alert-warning)
    else:
        return "rojo"      # Peligro (Bootstrap: alert-danger)