"""
Pruebas unitarias para la mejora: Botón Intercambiar unidades.
Verifica los criterios de aceptación:
- mm → m pasa a m → mm.
- Valor conserva exactamente el texto que tenía.
- El resultado vuelve a —.
- Pulsarlo dos veces restaura las unidades.
- Las pruebas anteriores siguen pasando.
"""

import unittest
from logica import intercambiar_unidades
from app import ConversorApp


class TestLogicaIntercambio(unittest.TestCase):
    def test_intercambio_unidades_basico(self):
        """Verifica que mm → m pase a m → mm."""
        orig, dest = "Milímetros (mm)", "Metros (m)"
        nuevo_orig, nuevo_dest = intercambiar_unidades(orig, dest)
        self.assertEqual(nuevo_orig, "Metros (m)")
        self.assertEqual(nuevo_dest, "Milímetros (mm)")

    def test_doble_intercambio_restaura_unidades(self):
        """Verifica que invocar dos veces la función restaure las unidades originales."""
        orig, dest = "Milímetros (mm)", "Metros (m)"
        orig_1, dest_1 = intercambiar_unidades(orig, dest)
        orig_2, dest_2 = intercambiar_unidades(orig_1, dest_1)
        self.assertEqual(orig_2, orig)
        self.assertEqual(dest_2, dest)


class TestComportamientoIntercambioApp(unittest.TestCase):
    def setUp(self):
        self.app = ConversorApp()
        self.app.update()

    def tearDown(self):
        try:
            for after_id in self.app.tk.eval('after info').split():
                self.app.after_cancel(after_id)
        except Exception:
            pass
        self.app.destroy()

    def test_comportamiento_boton_intercambiar(self):
        # 1. Configurar estado: mm → m con un valor específico
        self.app.var_origen.set("Milímetros (mm)")
        self.app.var_destino.set("Metros (m)")
        self.app.entry_valor.insert(0, "250")

        # 2. Convertir y comprobar que hay resultado visible
        self.app.accion_convertir()
        self.assertEqual(self.app.resultado_mostrado, "250 mm = 0,25 m")

        # 3. Pulsar botón intercambiar unidades
        self.app.accion_intercambiar()

        # Criterio: mm → m pasa a m → mm
        self.assertEqual(self.app.var_origen.get(), "Metros (m)")
        self.assertEqual(self.app.var_destino.get(), "Milímetros (mm)")

        # Criterio: Valor conserva exactamente el texto que tenía
        self.assertEqual(self.app.entry_valor.get(), "250")

        # Criterio: El resultado vuelve a —
        self.assertEqual(self.app.resultado_mostrado, "—")

        # 4. Pulsarlo dos veces restaura las unidades
        self.app.accion_intercambiar()
        self.assertEqual(self.app.var_origen.get(), "Milímetros (mm)")
        self.assertEqual(self.app.var_destino.get(), "Metros (m)")
        self.assertEqual(self.app.entry_valor.get(), "250")
        self.assertEqual(self.app.resultado_mostrado, "—")

    def test_convertir_despues_de_intercambiar(self):
        """Verifica que el botón Convertir funcione adecuadamente tras intercambiar."""
        self.app.var_origen.set("Metros (m)")
        self.app.var_destino.set("Centímetros (cm)")
        self.app.entry_valor.insert(0, "-2,5")

        # Convertir antes de intercambiar
        self.app.accion_convertir()
        self.assertEqual(self.app.resultado_mostrado, "-2,5 m = -250 cm")

        # Intercambiar unidades
        self.app.accion_intercambiar()
        self.assertEqual(self.app.var_origen.get(), "Centímetros (cm)")
        self.assertEqual(self.app.var_destino.get(), "Metros (m)")
        self.assertEqual(self.app.entry_valor.get(), "-2,5")
        self.assertEqual(self.app.resultado_mostrado, "—")

        # Convertir con las nuevas unidades
        self.app.accion_convertir()
        self.assertEqual(self.app.resultado_mostrado, "-2,5 cm = -0,025 m")


if __name__ == "__main__":
    unittest.main()
