import pandas as pd

#Para leer el archivo csv
def lector_archivo(ruta_archivo):
    df = pd.read_csv(ruta_archivo)
    return df

#Calcular el gasto total del csv
def calcular_total(df):
    total = df["monto"].sum()
    return total

#Calcular el gasto total por categoria
def calcular_por_categoria(df):
    categorias = df.groupby("categoria")
    totalcat = categorias["monto"].sum().to_dict()
    return totalcat

#Verificar si se supero el prespuesto o no
def verificar_presupuesto(total, presupuesto):
    superado = True
    if total > presupuesto:
        return superado
    else:
        superado = False
        return superado
    
