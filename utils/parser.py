"""
Utilidad para procesar funciones matemáticas ingresadas como texto
"""
import sympy as sp
import numpy as np
from typing import Tuple, Callable, Any

def procesar_funcion_personalizada(texto_funcion: str) -> Tuple[Callable, Callable, str, str]:
    """
    Convierte un string matemático en funciones de Python (f y f').
    
    Args:
        texto_funcion: String con la ecuación (ej: "x**2 - 4", "sin(x) + x")
        
    Returns:
        Tuple: (funcion_numpy, derivada_numpy, texto_derivada, mensaje_error)
    """
    try:
        # 1. Convertir texto a expresión simbólica
        # Se permiten funciones matemáticas comunes
        expr = sp.sympify(texto_funcion)
        
        # 2. Detectar la variable (x, n, lambda, etc.)
        simbolos = list(expr.free_symbols)
        
        if len(simbolos) > 1:
            return None, None, "", "Error: La función debe tener una sola variable (ej: x)"
        
        # Si es una constante (ej: "5"), asumimos x
        var = simbolos[0] if simbolos else sp.Symbol('x')
        
        # 3. Calcular derivada simbólica
        derivada_expr = sp.diff(expr, var)
        
        # 4. Convertir a funciones rápidas de Numpy (lambdify)
        # Esto permite evaluar f(x) con arrays o floats
        f_numpy = sp.lambdify(var, expr, modules=['numpy'])
        f_prime_numpy = sp.lambdify(var, derivada_expr, modules=['numpy'])
        
        # Wrapper para manejar escalares y arrays, y evitar problemas de dominio
        def f_segura(x):
            try:
                return f_numpy(x)
            except Exception as e:
                return float('nan')

        def f_prime_segura(x):
            try:
                return f_prime_numpy(x)
            except Exception as e:
                return float('nan')
                
        return f_segura, f_prime_segura, str(derivada_expr), None

    except sp.SympifyError:
        return None, None, "", "Error de sintaxis en la función"
    except Exception as e:
        return None, None, "", f"Error al procesar: {str(e)}"
