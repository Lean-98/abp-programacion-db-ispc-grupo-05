def campo_obligatorio(texto: str, nombre_campo: str):
    """Verifica que un campo no esté vacío."""
    if not texto or not str(texto).strip():
        raise ValueError(f"El campo '{nombre_campo}' es obligatorio.")

def campo_numerico(texto: str, nombre_campo: str):
    """Verifica que el campo sea numérico (solo dígitos)."""
    if not str(texto).strip().isdigit():
        raise ValueError(f"El campo '{nombre_campo}' debe contener solo números.")

def numero_entero_positivo(texto: str, nombre_campo: str):
    """Verifica que el campo sea un número entero positivo."""
    try:
        valor = int(texto)
        if valor < 0:
            raise ValueError()
        return valor
    except (ValueError, TypeError):
        raise ValueError(f"El campo '{nombre_campo}' debe ser un número entero positivo.")

def numero_decimal_positivo(texto: str, nombre_campo: str):
    """Verifica que el campo sea un número decimal positivo."""
    try:
        texto_limpio = str(texto).replace(",", ".")
        valor = float(texto_limpio)
        if valor < 0:
            raise ValueError()
        return valor
    except (ValueError, TypeError):
        raise ValueError(f"El campo '{nombre_campo}' debe ser un número decimal positivo.")

def validar_longitud_max(texto: str, nombre_campo: str, max_caracteres: int):
    """Valida la longitud máxima utilizando ValueError."""
    if len(texto) > max_caracteres:
        raise ValueError(f"El campo '{nombre_campo}' tiene un límite máximo de {max_caracteres} caracteres.")
    return True

