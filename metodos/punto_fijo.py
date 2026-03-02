"""
Método de Punto Fijo
Ejercicio 3: Crecimiento de Base de Datos
"""
import time
import numpy as np
from typing import Callable, Dict, List, Optional

def punto_fijo(
    g: Callable[[float], float],
    x0: float,
    tol: float = 1e-8,
    max_iter: int = 100,
    g_derivada: Optional[Callable] = None,
    limite_divergencia: float = 1e6
) -> Dict:
    """
    Implementación del método de punto fijo
    """
    start_time = time.time()
    
    # Verificar condición de convergencia si se proporciona derivada
    if g_derivada:
        try:
            g_prime_x0 = abs(g_derivada(x0))
            if g_prime_x0 >= 1:
                print(f"Advertencia: |g'(x0)| = {g_prime_x0:.4f} >= 1, "
                      f"puede no converger")
        except:
            pass
    
    iteraciones = []
    x_n = x0
    
    for n in range(1, max_iter + 1):
        # Calcular siguiente iteración
        x_next = g(x_n)
        
        # Verificar divergencia
        if abs(x_next) > limite_divergencia:
            return {
                'raiz': None,
                'iteraciones': iteraciones,
                'convergio': False,
                'iteraciones_totales': n,
                'error_final': float('inf'),
                'tiempo_ejecucion': time.time() - start_time,
                'mensaje': f"DIVERGENCIA: |x| > {limite_divergencia}"
            }
        
        # Cálculo de errores
        error_abs = abs(x_next - x_n)
        error_rel = error_abs / abs(x_next) if x_next != 0 else float('inf')
        diferencia = abs(x_next - x_n)
        
        # Guardar iteración
        iteracion = {
            'n': n,
            'x_n': x_n,
            'g(x_n)': x_next,
            'diferencia': diferencia,
            'error_abs': error_abs,
            'error_rel': error_rel
        }
        iteraciones.append(iteracion)
        
        # Verificar convergencia
        if diferencia < tol:
            break
        
        x_n = x_next
    
    elapsed_time = time.time() - start_time
    convergio = diferencia < tol and n < max_iter
    
    return {
        'raiz': x_next if convergio else None,
        'iteraciones': iteraciones,
        'convergio': convergio,
        'iteraciones_totales': n,
        'error_final': diferencia,
        'tiempo_ejecucion': elapsed_time,
        'mensaje': f"Raíz encontrada: {x_next:.8f} en {n} iteraciones" if convergio 
                  else f"No convergió después de {max_iter} iteraciones"
    }


def punto_fijo_multiple_inicial(
    g: Callable[[float], float],
    valores_iniciales: List[float],
    g_derivada: Optional[Callable] = None,
    tol: float = 1e-8
) -> Dict:
    """
    Ejecuta punto fijo con diferentes valores iniciales
    """
    resultados = {}
    for x0 in valores_iniciales:
        resultados[f"x0_{x0}"] = punto_fijo(g, x0, tol=tol, g_derivada=g_derivada)
    return resultados


def verificar_condicion_convergencia(
    g_derivada: Callable[[float], float],
    intervalo: List[float],
    n_puntos: int = 100
) -> Dict:
    """
    Verifica |g'(x)| < 1 en un intervalo
    """
    x_vals = np.linspace(intervalo[0], intervalo[1], n_puntos)
    g_prime_vals = [abs(g_derivada(x)) for x in x_vals]
    
    cumple_condicion = all(gp < 1 for gp in g_prime_vals)
    max_g_prime = max(g_prime_vals)
    
    return {
        'cumple_condicion': cumple_condicion,
        'max_g_prime': max_g_prime,
        'intervalo_verificado': intervalo,
        'recomendacion': "El método converge" if cumple_condicion 
                        else f"El método puede no converger |g'(x)| max = {max_g_prime:.4f}"
    }