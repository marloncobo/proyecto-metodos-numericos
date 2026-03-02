"""
Método de Falsa Posición (Regula Falsi)
Ejercicio 2: Balanceo de Carga
"""
import time
import numpy as np
from typing import Callable, Dict, List

def falsa_posicion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-7,
    max_iter: int = 100,
    error_tipo: str = 'absoluto'
) -> Dict:
    """
    Implementación del método de falsa posición
    """
    start_time = time.time()
    
    # Validaciones
    if a >= b:
        raise ValueError("El intervalo debe cumplir a < b")
    
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    
    iteraciones = []
    c_anterior = a
    
    for n in range(1, max_iter + 1):
        # Evitar división por cero
        if abs(fb - fa) < 1e-15:
            raise ValueError("División por cero en el cálculo de c")
        
        # Fórmula de falsa posición
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        
        # Cálculo de errores
        error_abs = abs(c - c_anterior)
        error_rel = error_abs / abs(c) if c != 0 else float('inf')
        error = error_abs if error_tipo == 'absoluto' else error_rel
        
        # Guardar iteración
        iteracion = {
            'n': n,
            'a': a,
            'b': b,
            'c': c,
            'f(a)': fa,
            'f(b)': fb,
            'f(c)': fc,
            'error_abs': error_abs,
            'error_rel': error_rel,
            'error': error
        }
        iteraciones.append(iteracion)
        
        # Verificar convergencia
        if abs(fc) < tol or error < tol:
            break
        
        # Actualizar intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        c_anterior = c
    
    elapsed_time = time.time() - start_time
    
    return {
        'raiz': c,
        'iteraciones': iteraciones,
        'convergio': n < max_iter or abs(fc) < tol,
        'iteraciones_totales': n,
        'error_final': error,
        'tiempo_ejecucion': elapsed_time,
        'mensaje': f"Raíz encontrada: {c:.8f} en {n} iteraciones"
    }


def comparar_biseccion_falsa_posicion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-7
) -> Dict:
    """
    Compara método de bisección con falsa posición
    """
    from metodos.biseccion import biseccion
    
    resultado_biseccion = biseccion(f, a, b, tol=tol)
    resultado_falsa = falsa_posicion(f, a, b, tol=tol)
    
    return {
        'biseccion': resultado_biseccion,
        'falsa_posicion': resultado_falsa,
        'comparacion': {
            'iteraciones_biseccion': resultado_biseccion['iteraciones_totales'],
            'iteraciones_falsa': resultado_falsa['iteraciones_totales'],
            'tiempo_biseccion': resultado_biseccion['tiempo_ejecucion'],
            'tiempo_falsa': resultado_falsa['tiempo_ejecucion'],
            'metodo_mas_rapido': 'falsa_posicion' if resultado_falsa['tiempo_ejecucion'] < resultado_biseccion['tiempo_ejecucion'] else 'biseccion'
        }
    }