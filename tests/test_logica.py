"""
Pruebas unitarias para el módulo logica.py del conversor de longitud.
Ejecuta la suite con: python -m unittest discover tests
"""

import unittest
from decimal import Decimal
from logica import (
    es_entrada_valida,
    validar_para_conversion,
    convertir_longitud,
    formatear_espanol
)


class TestValidacionEntrada(unittest.TestCase):
    def test_entradas_validas(self):
        """Verifica cadenas válidas completas y estados intermedios permitidos al escribir."""
        casos = [
            "25",
            "2,5",
            "2.5",
            "-10",
            "-2,75",
            "-0.5",
            "0",
            "",      # Al borrar todo
            "-",     # Al empezar a escribir número negativo
            ".",     # Al comenzar con punto decimal
            ",",     # Al comenzar con coma decimal
            "-.",    # Negativo con punto
            "-,"     # Negativo con coma
        ]
        for caso in casos:
            with self.subTest(caso=caso):
                self.assertTrue(
                    es_entrada_valida(caso),
                    f"'{caso}' debería ser aceptado por la validación de entrada"
                )

    def test_entradas_invalidas_bloqueadas(self):
        """Verifica que letras, símbolos extra y números mal formados sean bloqueados."""
        casos = [
            "abc",
            "12a",
            "3,4,5",
            "--5",
            "5-2",
            "2.3.4",
            "2.5,1",
            " ",
            "+5",
            "hello",
            "- 5"
        ]
        for caso in casos:
            with self.subTest(caso=caso):
                self.assertFalse(
                    es_entrada_valida(caso),
                    f"'{caso}' debería ser rechazado por la validación de entrada"
                )


class TestValidacionPreviaConversion(unittest.TestCase):
    def test_campo_vacio(self):
        """Campo vacío debe indicar el mensaje específico de introducir un valor."""
        valido, mensaje, valor = validar_para_conversion("")
        self.assertFalse(valido)
        self.assertEqual(mensaje, "Introduce un valor para realizar la conversión.")
        self.assertIsNone(valor)

        valido_espacios, mensaje_espacios, _ = validar_para_conversion("   ")
        self.assertFalse(valido_espacios)
        self.assertEqual(mensaje_espacios, "Introduce un valor para realizar la conversión.")

    def test_estados_incompletos(self):
        """Valores como solo '-', '.', ',' no son números completos para calcular."""
        casos_incompletos = ["-", ".", ",", "-.", "-,"]
        for caso in casos_incompletos:
            with self.subTest(caso=caso):
                valido, mensaje, valor = validar_para_conversion(caso)
                self.assertFalse(valido)
                self.assertEqual(mensaje, "Introduce un número válido.")
                self.assertIsNone(valor)

    def test_valores_validos_normalizados(self):
        """Valores válidos tanto con punto como con coma deben convertirse correctamente a Decimal."""
        valido_coma, _, val_coma = validar_para_conversion("2,5")
        self.assertTrue(valido_coma)
        self.assertEqual(val_coma, Decimal("2.5"))

        valido_punto, _, val_punto = validar_para_conversion("2.5")
        self.assertTrue(valido_punto)
        self.assertEqual(val_punto, Decimal("2.5"))

        valido_neg, _, val_neg = validar_para_conversion("-10")
        self.assertTrue(valido_neg)
        self.assertEqual(val_neg, Decimal("-10"))

        valido_cero, _, val_cero = validar_para_conversion("0")
        self.assertTrue(valido_cero)
        self.assertEqual(val_cero, Decimal("0"))


class TestCalculosConversion(unittest.TestCase):
    def test_casos_especificacion(self):
        """Comprueba exactamente los casos solicitados en la especificación."""
        casos = [
            # (valor_str, u_origen, u_destino, exp_orig, exp_dest, exp_resultado)
            ("1", "m", "cm", "1", "100", "1 m = 100 cm"),
            ("1", "m", "mm", "1", "1000", "1 m = 1000 mm"),
            ("1", "cm", "mm", "1", "10", "1 cm = 10 mm"),
            ("250", "mm", "cm", "250", "25", "250 mm = 25 cm"),
            ("150", "cm", "m", "150", "1,5", "150 cm = 1,5 m"),
            ("-2.5", "m", "cm", "-2,5", "-250", "-2,5 m = -250 cm"),
            ("0", "m", "cm", "0", "0", "0 m = 0 cm"),
        ]

        for val_str, orig, dest, exp_orig, exp_dest, exp_res in casos:
            with self.subTest(val=val_str, orig=orig, dest=dest):
                _, _, dec = validar_para_conversion(val_str)
                s_orig, s_dest, res_txt = convertir_longitud(dec, orig, dest)
                self.assertEqual(s_orig, exp_orig)
                self.assertEqual(s_dest, exp_dest)
                self.assertEqual(res_txt, exp_res)

    def test_misma_unidad_origen_y_destino(self):
        """Si origen y destino son iguales, el resultado debe coincidir con el valor introducido."""
        _, _, dec = validar_para_conversion("2,5")
        s_orig, s_dest, res_txt = convertir_longitud(dec, "m", "m")
        self.assertEqual(s_orig, "2,5")
        self.assertEqual(s_dest, "2,5")
        self.assertEqual(res_txt, "2,5 m = 2,5 m")

    def test_precision_decimal_sin_ceros_superfluos(self):
        """Verifica que se evite la imprecisión de coma flotante y se formatee limpiamente."""
        _, _, dec1 = validar_para_conversion("0,005")
        _, s_dest1, _ = convertir_longitud(dec1, "m", "mm")
        self.assertEqual(s_dest1, "5")

        _, _, dec2 = validar_para_conversion("1")
        _, s_dest2, _ = convertir_longitud(dec2, "mm", "m")
        self.assertEqual(s_dest2, "0,001")


class TestFormateoEspanol(unittest.TestCase):
    def test_formateo_coma_y_ceros(self):
        self.assertEqual(formatear_espanol(Decimal("2.5")), "2,5")
        self.assertEqual(formatear_espanol(Decimal("100.0")), "100")
        self.assertEqual(formatear_espanol(Decimal("-0")), "0")
        self.assertEqual(formatear_espanol(Decimal("0.0")), "0")
        self.assertEqual(formatear_espanol(Decimal("-250.75")), "-250,75")


if __name__ == "__main__":
    unittest.main()

