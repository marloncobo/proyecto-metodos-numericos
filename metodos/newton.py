"""
Método de Newton-Raphson
Ejercicio 4: Análisis de Concurrencia
"""
import time
import numpy as np
from typing import Callable, Dict, List, Optional

def newton_raphson(
    f: Callable[[float], float],
    f_derivada: Callable[[float], float],
    x0: float,
    tol: float = 1e-10,
    max_iter: int = 100,
    error_tipo: str = 'absoluto'
) -> Dict:
    """
    Implementación del método de Newton-Raphson
    """
    start_time = time.time()
    
    iteraciones = []
    x_n = x0
    errores_abs = []
    
    for n in range(1, max_iter + 1):
        f_xn = f(x_n)
        f_prime_xn = f_derivada(x_n)
        
        # Validar derivada no cero
        if abs(f_prime_xn) < 1e-15:
            return {
                'raiz': None,
                'iteraciones': iteraciones,
                'convergio': False,
                'iteraciones_totales': n,
                'error_final': float('inf'),
                'tiempo_ejecucion': time.time() - start_time,
                'mensaje': f"ERROR: Derivada casi cero en x = {x_n:.8f}"
            }
        
        # Fórmula de Newton-Raphson
        x_next = x_n - f_xn / f_prime_xn
        
        # Cálculo de errores
        error_abs = abs(x_next - x_n)
        error_rel = error_abs / abs(x_next) if x_next != 0 else float('inf')
        error = error_abs if error_tipo == 'absoluto' else error_rel
        errores_abs.append(error_abs)
        
        # Guardar iteración
        iteracion = {
            'n': n,
            'x_n': x_n,
            'f(x_n)': f_xn,
            "f'(x_n)": f_prime_xn,
            'x_next': x_next,
            'error_abs': error_abs,
            'error_rel': error_rel,
            'error': error
        }
        iteraciones.append(iteracion)
        
        # Verificar convergencia
        if error_abs < tol or abs(f_xn) < tol:
            break
        
        x_n = x_next
    
    elapsed_time = time.time() - start_time
    convergio = error_abs < tol and n < max_iter
    
    # Verificar convergencia cuadrática
    convergencia_cuadratica = verificar_convergencia_cuadratica(errores_abs)
    
    return {
        'raiz': x_next if convergio else None,
        'iteraciones': iteraciones,
        'convergio': convergio,
        'iteraciones_totales': n,
        'error_final': error_abs,
        'tiempo_ejecucion': elapsed_time,
        'convergencia_cuadratica': convergencia_cuadratica,
        'mensaje': f"Raíz encontrada: {x_next:.10f} en {n} iteraciones" if convergio
                  else f"No convergió después de {max_iter} iteraciones"
    }


def verificar_convergencia_cuadratica(errores: List[float]) -> Dict:
    """
    Verifica si el error muestra convergencia cuadrática
    """
    if len(errores) < 3:
        return {"es_cuadratica": False, "razon": "Insuficientes iteraciones"}
    
    razones = []
    for i in range(len(errores) - 2):
        if errores[i] > 0 and errores[i+1] > 0:
            razon = errores[i+1] / (errores[i] ** 2)
            razones.append(razon)
    
    if not razones:
        return {"es_cuadratica": False, "razon": "Errores cero"}
    
    razon_promedio = np.mean(razones)
    es_cuadratica = 0.1 < razon_promedio < 10  # Aproximadamente constante
    
    return {
        "es_cuadratica": es_cuadratica,
        "razon_promedio": razon_promedio,
        "razones": razones
    }


def newton_multiple_inicial(
    f: Callable[[float], float],
    f_derivada: Callable[[float], float],
    valores_iniciales: List[float],
    tol: float = 1e-10
) -> Dict:
    """
    Ejecuta Newton-Raphson con diferentes valores iniciales
    """
    resultados = {}
    for x0 in valores_iniciales:
        resultados[f"x0_{x0}"] = newton_raphson(f, f_derivada, x0, tol=tol)
    return resultados