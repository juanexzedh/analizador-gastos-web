import pandas as pd

def lector_archivo(ruta_archivo):
    df = pd.read_csv(ruta_archivo)
    return df

def calcular_total(df):
    total = df["monto"].sum()
    return total

def calcular_por_categoria(df):
    categorias = df.groupby("categoria")
    totalcat = categorias["monto"].sum().to_dict()
    return totalcat

def verificar_presupuesto(total, presupuesto):
    superado = True
    if total > presupuesto:
        return superado
    else:
        superado = False
        return superado
    
