"""
Módulo de lógica desacoplada para el conversor de unidades de longitud.
Contiene las funciones de validación de entrada, cálculo matemático de precisión
y formateo de valores para la presentación al usuario.
"""

import re
from decimal import Decimal, InvalidOperation

# Factores exactos de conversión con respecto al metro (m)
FACTORES_A_METROS = {
    "mm": Decimal("0.001"),
    "cm": Decimal("0.01"),
    "m":  Decimal("1")
}

ETIQUETAS_UNIDADES = {
    "Milímetros (mm)": "mm",
    "Centímetros (cm)": "cm",
    "Metros (m)": "m"
}

SIMBOLOS_A_ETIQUETAS = {v: k for k, v in ETIQUETAS_UNIDADES.items()}

# Expresión regular para validación en tiempo de escritura (bloqueo de pulsaciones)
# Permite únicamente: cadena vacía, '-' inicial, dígitos 0-9 y máximo una coma o punto.
REGEX_ENTRADA_VALIDA = re.compile(r'^-?[0-9]*[.,]?[0-9]*$')


def es_entrada_valida(texto: str) -> bool:
    """
    Verifica si una cadena cumple con la regla de escritura permitida en el campo.
    Acepta estados parciales válidos durante la edición (ej. '-', '.', '2,', '-5.').
    """
    return bool(REGEX_ENTRADA_VALIDA.fullmatch(texto))


def formatear_espanol(valor: Decimal) -> str:
    """
    Convierte un Decimal a cadena de texto con formato español:
    - Utiliza la coma ',' como separador decimal.
    - Evita notación científica.
    - Suprime ceros innecesarios a la derecha tras el separador.
    - Convierte '-0' a '0'.
    """
    cadena = format(valor, "f")
    if "." in cadena:
        cadena = cadena.rstrip("0").rstrip(".")
    if cadena == "-0" or cadena == "":
        cadena = "0"
    return cadena.replace(".", ",")


def validar_para_conversion(texto: str):
    """
    Valida si el contenido del campo es apto para realizar un cálculo.
    Devuelve: (es_valido: bool, mensaje_error: str, valor_decimal: Decimal | None)
    """
    texto_limpio = texto.strip()

    if not texto_limpio:
        return False, "Introduce un valor para realizar la conversión.", None

    if texto_limpio in ("-", ".", ",", "-.", "-,"):
        return False, "Introduce un número válido.", None

    # Normalizar coma a punto antes de procesar con Decimal
    normalizado = texto_limpio.replace(",", ".")
    try:
        val_decimal = Decimal(normalizado)
        return True, "", val_decimal
    except (InvalidOperation, ValueError):
        return False, "Introduce un número válido.", None


def convertir_longitud(valor_decimal: Decimal, unidad_origen: str, unidad_destino: str):
    """
    Realiza la conversión entre las unidades especificadas ('mm', 'cm', 'm')
    utilizando precisión exacta Decimal.
    Devuelve: (valor_origen_formateado, valor_destino_formateado, texto_resultado)
    """
    if unidad_origen not in FACTORES_A_METROS or unidad_destino not in FACTORES_A_METROS:
        raise ValueError(f"Unidades no soportadas: {unidad_origen} -> {unidad_destino}")

    factor_origen = FACTORES_A_METROS[unidad_origen]
    factor_destino = FACTORES_A_METROS[unidad_destino]

    # Conversión a metros y luego a la unidad de destino
    metros = valor_decimal * factor_origen
    resultado_decimal = metros / factor_destino

    str_origen = formatear_espanol(valor_decimal)
    str_destino = formatear_espanol(resultado_decimal)
    texto_resultado = f"{str_origen} {unidad_origen} = {str_destino} {unidad_destino}"

    return str_origen, str_destino, texto_resultado

