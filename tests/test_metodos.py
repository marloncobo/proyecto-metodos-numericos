# tests/test_metodos.py
import unittest
import numpy as np
from funciones.definiciones import T_lambda, E_workers
from metodos.biseccion import biseccion
from metodos.falsa_posicion import falsa_posicion
from metodos.newton import newton_raphson
from metodos.punto_fijo import punto_fijo
from metodos.secante import secante

class TestMetodosNumericos(unittest.TestCase):

    def test_biseccion(self):
        # Usando Ejercicio 1
        f = lambda x: x ** 2 - 4
        resultado = biseccion(f, 0.0, 3.0, tol=1e-6)
        self.assertTrue(resultado['convergio'])
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=5)

    def test_falsa_posicion(self):
        # Usando Ejercicio 2
        resultado = falsa_posicion(E_workers, 2.0, 4.0, tol=1e-7)
        self.assertTrue(resultado['convergio'])
        self.assertAlmostEqual(E_workers(resultado['raiz']), 0, places=5)

    def test_newton_raphson(self):
        # Usando función simple f(x) = x^2 - 4, f'(x) = 2x
        f = lambda x: x**2 - 4
        f_prime = lambda x: 2*x
        resultado = newton_raphson(f, f_prime, 3.0, tol=1e-10)
        self.assertTrue(resultado['convergio'])
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=8)

if __name__ == '__main__':
    unittest.main()