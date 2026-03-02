"""
Método de Bisección
Ejercicio 1: Optimización de Hash Table
"""
import numpy as np
import time
from typing import Callable, Dict, List, Tuple, Optional

def biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 100,
    error_tipo: str = 'absoluto'
) -> Dict:
    """
    Implementación del método de bisección
    
    Args:
        f: Función a evaluar
        a: Extremo izquierdo del intervalo
        b: Extremo derecho del intervalo
        tol: Tolerancia para el criterio de parada
        max_iter: Número máximo de iteraciones
        error_tipo: 'absoluto' o 'relativo'
    
    Returns:
        Diccionario con resultados del método
    """
    start_time = time.time()
    
    # Validaciones iniciales
    if a >= b:
        raise ValueError("El intervalo debe cumplir a < b")
    
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    
    # Inicialización
    iteraciones = []
    c_anterior = a
    
    for n in range(1, max_iter + 1):
        # Punto medio
        c = (a + b) / 2
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


def biseccion_con_comparacion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tolerancias: List[float] = [1e-4, 1e-6, 1e-8]
) -> Dict:
    """
    Ejecuta bisección con diferentes tolerancias para comparación
    """
    resultados = {}
    for tol in tolerancias:
        resultados[f"tol_{tol}"] = biseccion(f, a, b, tol=tol)
    return resultados