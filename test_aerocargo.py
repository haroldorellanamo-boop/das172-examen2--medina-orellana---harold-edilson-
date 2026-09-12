"""
Casos de prueba unitaria y verificacion de limites para AeroCargo-Matrix.
"""
import unittest
from aerocargo_matrix import (
    validar_coherencia,
    calcular_ocupacion,
    evaluar_balance,
    extraer_submatriz_critica
)

class TestAeroCargo(unittest.TestCase):

    def setUp(self):
        self.cargas_par = [
            [200.0, 300.0, 250.0, 200.0],
            [100.0, 450.0, 400.0, 150.0]
        ]
        self.cap_par = [
            [250.0, 300.0, 300.0, 250.0],
            [200.0, 400.0, 400.0, 200.0]
        ]

    def test_validacion_correcta(self):
        self.assertTrue(validar_coherencia(self.cargas_par, self.cap_par))

    def test_validacion_fallo_dimensiones_menores(self):
        self.assertFalse(validar_coherencia([[100, 200]], [[100, 200]]))

    def test_validacion_capacidad_cero_o_negativa(self):
        cap_invalida = [[200.0, 0.0], [200.0, 200.0]]
        carga_valida = [[100.0, 100.0], [100.0, 100.0]]
        self.assertFalse(validar_coherencia(carga_valida, cap_invalida))

    def test_ocupacion_y_sobrecarga(self):
        res = calcular_ocupacion(self.cargas_par, self.cap_par)
        self.assertIn((1, 1), res["celdas_sobrecarga"])
        self.assertEqual(res["matriz_ocupacion"][0][0], 80.0)

    def test_balance_lateral_columnas_pares(self):
        res = evaluar_balance(self.cargas_par, tolerancia_kg=60.0)
        self.assertEqual(res["desbalance_lateral"], 50.0)
        self.assertTrue(res["balance_aprobado"])

    def test_balance_lateral_columnas_impares(self):
        cargas_impar = [
            [100.0, 999.0, 120.0],
            [200.0, 888.0, 210.0]
        ]
        res = evaluar_balance(cargas_impar, tolerancia_kg=25.0)
        self.assertEqual(res["desbalance_lateral"], 30.0)
        self.assertFalse(res["balance_aprobado"])

    def test_extraccion_submatriz(self):
        matriz = [
            [10.0, 20.0, 30.0],
            [40.0, 90.0, 95.0],
            [10.0, 85.0, 100.0]
        ]
        sub = extraer_submatriz_critica(matriz, 2, 2)
        esperado = [
            [90.0, 95.0],
            [85.0, 100.0]
        ]
        self.assertEqual(sub, esperado)

if __name__ == "__main__":
    unittest.main()
