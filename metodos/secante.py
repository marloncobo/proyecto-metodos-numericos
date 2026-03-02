"""
Método de la Secante
Ejercicio 5: Predicción de Escalabilidad
"""
import time
import numpy as np
from typing import Callable, Dict, List, Optional

def secante(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-9,
    max_iter: int = 100,
    error_tipo: str = 'absoluto'
) -> Dict:
    """
    Implementación del método de la secante
    """
    start_time = time.time()
    
    iteraciones = []
    x_prev = x0
    x_curr = x1
    
    try:
        f_prev = f(x_prev)
    except:
        f_prev = float('nan')
        
    evaluaciones_funcion = 2  # x0 y x1 ya evaluadas (o intentadas)
    
    for n in range(1, max_iter + 1):
        try:
            f_curr = f(x_curr)
        except:
            f_curr = float('nan')
            
        evaluaciones_funcion += 1
        
        # Validar si la función devolvió NaN (fuera de dominio, etc.)
        if np.isnan(f_curr) or np.isnan(f_prev):
             return {
                'raiz': None,
                'iteraciones': iteraciones,
                'convergio': False,
                'iteraciones_totales': n,
                'evaluaciones_funcion': evaluaciones_funcion,
                'error_final': float('inf'),
                'tiempo_ejecucion': time.time() - start_time,
                'mensaje': f"ERROR: Función indefinida (NaN) en iteración {n}. Posiblemente fuera de dominio."
            }

        # Validar diferencia no cero
        if abs(f_curr - f_prev) < 1e-15:
            return {
                'raiz': None,
                'iteraciones': iteraciones,
                'convergio': False,
                'iteraciones_totales': n,
                'evaluaciones_funcion': evaluaciones_funcion,
                'error_final': float('inf'),
                'tiempo_ejecucion': time.time() - start_time,
                'mensaje': f"ERROR: Diferencia de funciones casi cero"
            }
        
        # Fórmula de la secante
        try:
            x_next = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
        except ZeroDivisionError:
             return {
                'raiz': None,
                'iteraciones': iteraciones,
                'convergio': False,
                'iteraciones_totales': n,
                'evaluaciones_funcion': evaluaciones_funcion,
                'error_final': float('inf'),
                'tiempo_ejecucion': time.time() - start_time,
                'mensaje': f"ERROR: División por cero"
            }

        # Cálculo de errores
        error_abs = abs(x_next - x_curr)
        error_rel = error_abs / abs(x_next) if x_next != 0 else float('inf')
        error = error_abs if error_tipo == 'absoluto' else error_rel
        
        # Guardar iteración
        iteracion = {
            'n': n,
            'x_{n-1}': x_prev,
            'x_n': x_curr,
            'f(x_{n-1})': f_prev,
            'f(x_n)': f_curr,
            'x_{n+1}': x_next,
            'error_abs': error_abs,
            'error_rel': error_rel,
            'error': error
        }
        iteraciones.append(iteracion)
        
        # Verificar convergencia
        if error_abs < tol or abs(f_curr) < tol:
            break
        
        # Actualizar para siguiente iteración
        x_prev = x_curr
        x_curr = x_next
        f_prev = f_curr
    
    elapsed_time = time.time() - start_time
    convergio = error_abs < tol and n < max_iter
    
    return {
        'raiz': x_next if convergio else None,
        'iteraciones': iteraciones,
        'convergio': convergio,
        'iteraciones_totales': n,
        'evaluaciones_funcion': evaluaciones_funcion,
        'error_final': error_abs,
        'tiempo_ejecucion': elapsed_time,
        'mensaje': f"Raíz encontrada: {x_next:.9f} en {n} iteraciones" if convergio
                  else f"No convergió después de {max_iter} iteraciones"
    }


def comparar_newton_secante(
    f: Callable[[float], float],
    f_derivada: Callable[[float], float],
    x0_newton: float,
    x0_secante: float,
    x1_secante: float,
    tol: float = 1e-9
) -> Dict:
    """
    Compara método de Newton-Raphson con secante
    """
    from metodos.newton import newton_raphson
    
    resultado_newton = newton_raphson(f, f_derivada, x0_newton, tol=tol)
    resultado_secante = secante(f, x0_secante, x1_secante, tol=tol)
    
    return {
        'newton': resultado_newton,
        'secante': resultado_secante,
        'comparacion': {
            'iteraciones_newton': resultado_newton['iteraciones_totales'],
            'iteraciones_secante': resultado_secante['iteraciones_totales'],
            'evaluaciones_newton': resultado_newton['iteraciones_totales'] * 2,  # f y f'
            'evaluaciones_secante': resultado_secante['evaluaciones_funcion'],
            'tiempo_newton': resultado_newton['tiempo_ejecucion'],
            'tiempo_secante': resultado_secante['tiempo_ejecucion'],
            'metodo_mas_rapido': 'newton' if resultado_newton['tiempo_ejecucion'] < resultado_secante['tiempo_ejecucion'] else 'secante',
            'metodo_menos_evaluaciones': 'newton' if resultado_newton['iteraciones_totales'] * 2 < resultado_secante['evaluaciones_funcion'] else 'secante'
        }
    }