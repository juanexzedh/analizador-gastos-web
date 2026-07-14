# Diccionario identificar categorias automáticamente
CATEGORIAS_MAPEADAS = {
    'Alimentación': ['rappi', 'restaurante', 'comida', 'jumbo', 'exito', 'carulla', 'd1', 'ara', 'cafeteria', 'panaderia'],
    'Transporte': ['uber', 'cabify', 'transmilenio', 'gasolina', 'taxis', 'peaje', 'didi'],
    'Entretenimiento': ['netflix', 'spotify', 'cine', 'disney', 'hbo', 'concierto', 'bar', 'fiesta'],
    'Servicios': ['claro', 'movistar', 'enel', 'acueducto', 'vanti', 'internet', 'gas'],
    'Educación': ['universidad', 'ean', 'curso', 'platzi', 'udemy', 'libros'],
    'Salud': ['drogueria', 'eps', 'medico', 'farmacia', 'odontologo'],
    'Hogar': ['arriendo', 'administracion', 'muebles', 'ferreteria']
}

def categorizar(descripcion):
    # Analiza la descripcion de texto y devuelve la categoria sugerida
    if not descripcion or not isinstance(descripcion, str):
        return 'Otro'
    desc_lower = descripcion.lower()
    
    for categoria, palabras_clave in CATEGORIAS_MAPEADAS.items():
        if any(palabra in desc_lower for palabra in palabras_clave):
            return categoria
            
    return 'Otro'