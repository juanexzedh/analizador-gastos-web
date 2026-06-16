from flask import Flask, render_template, request
from servicios.analizador import lector_archivo, calcular_total, calcular_por_categoria, verificar_presupuesto
#Se importan las funciones del analizador

# Inicializar flask
app = Flask(__name__)

# Ruta a la pagina principal
@app.route("/")
def inicio():
    return render_template("index.html")

# Procesa el csv subido 
@app.route("/analizar", methods=["POST"])
def analizar():
    #Obtiene el archivo y el presupuesto del forms
    archivo = request.files["archivo"] 
    presupuesto = request.form["presupuesto"]
    print(f"Archivo: {archivo.filename}, Prespupuesto: {presupuesto}")

    #guarda el archivo, y crea una variable para la ruta de donde se guardo
    ruta_archivo = f"uploads/{archivo.filename}"
    archivo.save(ruta_archivo)

    #lee el archivo csv
    df = lector_archivo(ruta_archivo)
    #Total de los gastos
    total = calcular_total(df)
    #Total por categoria
    totalxcategoria = calcular_por_categoria(df)
    #Verificar resultado
    resultado = verificar_presupuesto(total, int(presupuesto))
    
    print(df.head())
    print(f"Total de los gastos: {total}")
    print(f"Gastos por Categoria: {totalxcategoria}")
    print(type(totalxcategoria))
    print(f"¿Se supero el presupuesto?: {resultado}")

    return render_template("resultado.html", 
                           total = total, 
                           totalxcategoria = totalxcategoria, 
                           resultado = resultado, 
                           presupuesto = presupuesto)

#Ejecutar la aplicacion
if __name__ == "__main__":
    app.run(debug=True)