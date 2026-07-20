import sqlite3
import os

DB_PATH = os.path.join('data', 'gastos.db')

def obtener_conexion():
    #Garantiza que la carpeta 'data' exista y retorna la conexion a SQLite
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Row_factory permite acceder a los datos por nombre de columna: fila['monto']
    conn.row_factory = sqlite3.Row 
    return conn

def inicializar_db():
    """Crea las tablas necesarias si no existen al iniciar la aplicación."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Tabla de movimientos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,         -- Fecha exacta (YYYY-MM-DD)
            descripcion TEXT NOT NULL,
            categoria TEXT,
            monto REAL NOT NULL,
            tipo TEXT NOT NULL,          -- 'gasto' o 'ingreso'
            periodo TEXT NOT NULL        -- Periodo (YYYY-MM)
        )
    ''')
    conn.commit()
    conn.close()

def guardar_gastos(lista_movimientos, periodo):
    #Guarda una lista de diccionarios en la base de datos.
    #Primero limpia el periodo para evitar duplicados si se resube el archivo.
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Eliminar datos anteriores de este periodo para sobreescribir limpiamente
    cursor.execute("DELETE FROM gastos WHERE periodo = ?", (periodo,))
    
    # Insertar la lista de movimientos
    for mov in lista_movimientos:
        cursor.execute('''
            INSERT INTO gastos (fecha, descripcion, categoria, monto, tipo, periodo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            mov['fecha'],
            mov['descripcion'],
            mov.get('categoria', 'Otro') or 'Otro',
            float(mov['monto']),
            mov['tipo'].lower(),
            periodo
        ))
    conn.commit()
    conn.close()

def obtener_gastos(periodo):
    #Recupera los movimientos de un periodo específico (YYYY-MM).
    #Retorna una lista de diccionarios nativos de Python.
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT fecha, descripcion, categoria, monto, tipo FROM gastos WHERE periodo = ? ORDER BY fecha ASC",
        (periodo,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    # Se convierte el resultado de SQLite en una lista de diccionarios estandar
    return [dict(row) for row in rows]

def obtener_periodos_disponibles():
    #Retorna una lista de strings con los periodos guardados (ej: ['2026-07', '2026-06'])
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT periodo FROM gastos ORDER BY periodo DESC")
    periodos = cursor.fetchall()
    conn.close()
    return [row['periodo'] for row in periodos]

def obtener_resumen_periodos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    consulta = """
        SELECT 
            periodo,
            SUM(CASE WHEN tipo = 'gasto' THEN monto ELSE 0 END) as total_gastos,
            SUM(CASE WHEN tipo = 'ingreso' THEN monto ELSE 0 END) as total_ingresos
        FROM gastos
        GROUP BY periodo
        ORDER BY periodo DESC
    """
    cursor.execute(consulta)
    filas = cursor.fetchall()
    conn.close()
    
    resumen = []
    for fila in filas:
        periodo = fila['periodo']
        anio, mes = periodo.split('-') if '-' in periodo else (periodo, "")
        
        gastos = fila['total_gastos'] or 0
        ingresos = fila['total_ingresos'] or 0
        balance = ingresos - gastos
        
        resumen.append({
            'periodo': periodo,
            'mes': mes,
            'anio': anio,
            'gastos': gastos,
            'ingresos': ingresos,
            'balance': balance
        })
        
    return resumen

def vaciar_registros():
    #Elimina todos los registros de la tabla
    conn = obterner_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("DELETE FROM gastos")
        conn.commit()
        print("¡Todos los registros han sido eliminados de forma exitosa!")
    except sqlite3.Error as e:
        print(f"Error al vaciar la tabla: {e}")
    finally:
        conn.close()