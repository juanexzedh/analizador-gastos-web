# 📈 Asistente Financiero Web

Una aplicación web desarrollada en **Python** con **Flask** para la gestión, análisis y predicción de finanzas personales. El sistema permite a los usuarios procesar sus estados financieros mediante archivos Excel, almacenar el historial en una base de datos local y utilizar modelos de **Machine Learning** para estimar el comportamiento futuro de sus gastos.

---

## 🚀 Características Principales

### 📊 Procesamiento de Datos (Pandas)

- Lectura e interpretación de archivos Excel (`.xlsx`).
- Procesamiento automático de ingresos y gastos.
- Agrupación de gastos por categoría.
- Comparación entre periodos utilizando `pd.merge()`.
- Cálculo de variaciones absolutas y porcentuales entre meses.

### 🗄️ Persistencia de Datos (SQLite3)

A diferencia de un simple procesador de archivos, el sistema almacena permanentemente la información financiera en una base de datos SQLite.

Esto permite:

- Mantener un historial financiero.
- Consultar meses anteriores sin volver a cargar archivos.
- Comparar distintos periodos.
- Alimentar el modelo de Machine Learning con datos históricos.

### 🤖 Predicción Inteligente (Scikit-Learn)

El sistema incorpora un modelo de **Regresión Lineal (LinearRegression)** que analiza el comportamiento histórico de los gastos.

Características:

- Se activa automáticamente cuando existen **mínimo 3 meses registrados**.
- Predice el gasto esperado del siguiente mes.
- Utiliza la tendencia histórica para generar una proyección matemática.

### 📄 Reportes Descargables (ReportLab)

Generación dinámica de reportes PDF que incluyen:

- Resumen financiero.
- Tabla de ingresos y gastos.
- Top 5 gastos más altos.
- Semáforo financiero.
- Indicadores del periodo seleccionado.

Todos los documentos se generan completamente en memoria utilizando **BytesIO**, evitando crear archivos temporales en el servidor.

### 📈 Proyección de Fin de Mes

Durante el mes actual el sistema calcula:

- Promedio diario de gasto.
- Proyección matemática del gasto al finalizar el mes.
- Comparación entre el presupuesto actual y el proyectado.

Esto permite al usuario detectar posibles excesos antes de terminar el mes.

---

# 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|------------|-----|
| Flask | Framework Backend |
| Pandas | Procesamiento de datos |
| SQLite3 | Base de datos |
| OpenPyXL | Lectura de archivos Excel |
| Scikit-Learn | Machine Learning |
| ReportLab | Generación de PDF |
| HTML5 | Interfaz |
| Bootstrap 5 | Diseño Responsive |
| Jinja2 | Plantillas HTML |

---

# 📂 Estructura del Proyecto

```text
Asistente-Financiero/
│
├── app.py
├── requirements.txt
├── README.md
│
├── images/
│   └── finanzas.db
│
├── servicios/
    ├── analizador.py
│   ├── categorizer.py
│   ├── database.py
│   ├── pdf_doc.py
│   └── predictor.py
│
├── reportes/
│
├── static/
│   ├── css/styles.css
│   ├── assets/plantilla.xlsx
│   └── js/
│
├── templates/
│   ├── index.html
│   ├── historial.html
│   ├── instructivo.html
│   └── resultado.html
│
└── 
```

---

# ⚙️ Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/juanexzedh/analizador-gastos-web
cd asistente-financiero
```

---

## 2. Crear un entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install requirements
```

---

## 4. Ejecutar el proyecto

```bash
python app.py
```

La aplicación estará disponible en:

```
http://127.0.0.1:5000
```

---

# 📖 Flujo de Uso del Sistema

El sistema está diseñado para fortalecerse conforme el usuario incorpora nuevos periodos financieros.

---

# 1️⃣ Página de Inicio

Desde la pantalla principal el usuario puede cargar un archivo Excel con la información financiera del mes.

También encontrará un acceso directo al instructivo, donde se especifica el formato exacto que debe tener el archivo para ser procesado correctamente.

## Vista

<!-- ============================ -->
<!-- INSERTAR IMAGEN AQUÍ -->
<!-- Página de Inicio -->
<!-- static/screenshots/inicio.png -->
<!-- ============================ -->

---

# 2️⃣ Instructivo

Antes de cargar un archivo, el usuario puede descargar una plantilla e instrucciones donde se explica el formato requerido.

Las columnas esperadas son:

| fecha | descripcion | categoria | monto | tipo |
|-------|-------------|-----------|------:|------|

Este formato garantiza que Pandas pueda interpretar correctamente la información.

## Vista

<!-- ============================ -->
<!-- INSERTAR IMAGEN AQUÍ -->
<!-- Instructivo -->
<!-- static/screenshots/instructivo.png -->
<!-- ============================ -->

---

# 3️⃣ Carga del Archivo de Agosto

Para este ejemplo se carga el archivo correspondiente al mes de Agosto.

Se asume que el mes de Julio ya había sido procesado anteriormente y permanece almacenado dentro de SQLite.

Al subir el archivo, Pandas realiza:

- lectura del Excel
- validación de columnas
- separación entre ingresos y gastos
- almacenamiento en la base de datos

## Vista

<!-- ============================ -->
<!-- INSERTAR IMAGEN AQUÍ -->
<!-- Esquema Excel Agosto -->
<!-- static/screenshots/esquema_agosto.png -->
<!-- ============================ -->

---

# 4️⃣ Dashboard de Resultados (Agosto)

Una vez procesado el archivo, el Dashboard muestra:

- Total de ingresos
- Total de gastos
- Capital ahorrado
- Gastos por categoría
- Proyección de gasto del mes

Como únicamente existen dos meses registrados (Julio y Agosto), el modelo de Machine Learning todavía no puede generar predicciones.

El sistema informa al usuario que necesita un tercer periodo para habilitar dicha funcionalidad.

## Vista

<!-- ============================ -->
<!-- INSERTAR IMAGEN AQUÍ -->
<!-- Resultados Agosto -->
<!-- static/screenshots/dashboard_agosto.png -->
<!-- ============================ -->

---

# 5️⃣ Generación del Reporte PDF

El usuario puede descargar un reporte completo del periodo.

El documento contiene:

- Resumen financiero
- Semáforo financiero
- Top 5 gastos
- Totales
- Indicadores

Todo el PDF es generado dinámicamente mediante ReportLab.

## Vista

<!-- ============================ -->
<!-- INSERTAR IMAGEN AQUÍ -->
<!-- Documento PDF -->
<!-- static/screenshots/pdf.png -->
<!-- ============================ -->

---

# 6️⃣ Historial y Comparación

El sistema conserva automáticamente todos los periodos procesados.

Desde la sección Historial el usuario puede consultar cada uno de ellos y seleccionar dos meses para compararlos.

Internamente el backend utiliza:

```python
pd.merge()
```

para comparar categorías entre ambos meses.

Posteriormente calcula:

- diferencia absoluta
- variación porcentual

Los resultados se presentan mediante colores condicionales:

🟢 Disminución del gasto

🔴 Incremento del gasto

## Vista

<!-- ============================ -->
<!-- INSERTAR IMAGEN AQUÍ -->
<!-- Historial -->
<!-- static/screenshots/historial.png -->
<!-- ============================ -->

<br>

<!-- ============================ -->
<!-- INSERTAR IMAGEN AQUÍ -->
<!-- Comparación Julio Agosto -->
<!-- static/screenshots/comparacion.png -->
<!-- ============================ -->

---

# 7️⃣ Resultados de Septiembre (Machine Learning)

Cuando el usuario procesa el archivo correspondiente a Septiembre, el sistema ya dispone de tres periodos completos:

- Julio
- Agosto
- Septiembre

Esta condición activa automáticamente el modelo de **LinearRegression**.

Ahora el Dashboard incorpora una nueva sección donde estima matemáticamente el gasto esperado para Octubre.

La predicción se basa exclusivamente en el comportamiento histórico almacenado en la base de datos.

## Vista

<!-- ============================ -->
<!-- INSERTAR IMAGEN AQUÍ -->
<!-- Dashboard Septiembre -->
<!-- static/screenshots/dashboard_septiembre.png -->
<!-- ============================ -->

---

# 🧠 Machine Learning

El modelo utilizado corresponde a una **Regresión Lineal** implementada mediante **Scikit-Learn**.

Flujo de entrenamiento:

```
Julio
      \
Agosto ---> Modelo LinearRegression ---> Predicción Octubre
      /
Septiembre
```

El entrenamiento se realiza únicamente cuando existen al menos tres meses registrados.

---

# 📊 Funcionalidades Implementadas

- ✅ Lectura de archivos Excel
- ✅ Validación de formato
- ✅ Almacenamiento en SQLite
- ✅ Dashboard financiero
- ✅ Clasificación de gastos
- ✅ Comparación entre meses
- ✅ Reportes PDF
- ✅ Proyección de gasto mensual
- ✅ Predicción mediante Machine Learning
- ✅ Historial financiero

---

# 👨‍💻 Autor

Juan Esteban Hernandez Gualtero

Aplicando aptitudes como:
- Ciencia de Datos
- Machine Learning
- Desarrollo Web con Flask
- Procesamiento de datos con Pandas
- Bases de Datos SQLite