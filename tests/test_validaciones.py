"""Pruebas unitarias básicas y reproducibles de las validaciones principales."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import validaciones as v
from reportes import promedio_dias_respuesta_entero

class TestValidaciones(unittest.TestCase):
    def test_nombre(self):
        self.assertTrue(v.validar_nombre("María José Pérez")[0])
        self.assertFalse(v.validar_nombre("Juan123")[0])

    def test_documento_y_telefono(self):
        self.assertTrue(v.validar_numero_documento("1037654321")[0])
        self.assertFalse(v.validar_numero_documento("10376A321")[0])
        self.assertTrue(v.validar_telefono("3001234567")[0])
        self.assertFalse(v.validar_telefono("300123ABCD")[0])

    def test_correo_y_perfil(self):
        self.assertTrue(v.validar_correo("usuario@correo.com")[0])
        self.assertFalse(v.validar_correo("usuariocorreo.com")[0])
        self.assertTrue(v.validar_perfil_solicitante("Docente")[0])

    def test_fecha_futura_y_direccion(self):
        self.assertFalse(v.validar_fecha_radicacion("2999-01-01")[0])
        self.assertEqual(v.validar_direccion("")[1], "N/A")

    def test_flujo_estado(self):
        self.assertTrue(v.validar_transicion_estado("Registrada", "En proceso")[0])
        self.assertFalse(v.validar_transicion_estado("Registrada", "Solucionada")[0])

    def test_promedio_no_inventa_fecha_solucion(self):
        datos = [
            {"fecha_radicacion": "2026-01-01 00:00:00", "fecha_solucion": "2026-01-04 00:00:00", "estado_peticion": "Solucionada"},
            {"fecha_radicacion": "2026-01-01 00:00:00", "fecha_solucion": "", "estado_peticion": "Solucionada"},
        ]
        self.assertEqual(promedio_dias_respuesta_entero(datos), 3)

if __name__ == "__main__":
    unittest.main(verbosity=2)
