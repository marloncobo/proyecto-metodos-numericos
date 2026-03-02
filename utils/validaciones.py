"""
Funciones de validación para los métodos numéricos
"""
import numpy as np
from typing import Callable, Tuple, Union, List, Dict

def validar_intervalo_raiz(
    f: Callable[[float], float],
    a: float,
    b: float,
    n_puntos: int = 100
) -> Tuple[bool, str]:
    """
    Verifica si existe una raíz en el intervalo [a, b] y si el dominio es válido.
    """
    if a >= b:
        return False, "El intervalo debe cumplir a < b"
    
    try:
        # Intentar evaluar en los extremos
        # Usamos np.seterr para capturar advertencias como errores si es necesario,
        # pero el try-except general suele bastar para errores de python puro.
        fa = f(a)
        fb = f(b)
    except Exception as e:
        return False, f"Error matemático al evaluar extremos: {str(e)}"
    
    # Verificar si los valores son válidos (no NaN ni Infinito)
    if np.isnan(fa) or np.isnan(fb):
        return False, "CRÍTICO: La función no está definida en uno de los extremos (NaN). Verifique el dominio."
    
    if np.isinf(fa) or np.isinf(fb):
        return False, "CRÍTICO: La función tiende a infinito en uno de los extremos."
    
    # Verificación de Bolzano (Cambio de signo)
    if fa * fb < 0:
        return True, "Existe al menos una raíz en el intervalo"
    elif fa == 0:
        return True, f"a = {a} es una raíz"
    elif fb == 0:
        return True, f"b = {b} es una raíz"
    else:
        # Verificar cambios de signo en puntos intermedios
        try:
            x_vals = np.linspace(a, b, n_puntos)
            y_vals = [f(x) for x in x_vals]
            
            # Verificar si algún punto intermedio es inválido
            if any(np.isnan(y) or np.isinf(y) for y in y_vals):
                 return False, "CRÍTICO: La función se indefine dentro del intervalo seleccionado."

            for i in range(len(y_vals) - 1):
                if y_vals[i] * y_vals[i + 1] < 0:
                    return True, f"Existe raíz en subintervalo [{x_vals[i]:.3f}, {x_vals[i+1]:.3f}]"
        except:
            pass # Si falla el linspace, nos quedamos con el fallo de extremos
        
        return False, "No se detectó cambio de signo en el intervalo (puede no haber raíz)"


def validar_tolerancia(tol: Union[float, str]) -> Tuple[bool, float, str]:
    """
    Valida que la tolerancia sea un número positivo
    """
    try:
        tol = float(tol)
        if tol <= 0:
            return False, 0, "La tolerancia debe ser positiva"
        if tol < 1e-15:
            return False, 0, "La tolerancia es demasiado pequeña (mínimo 1e-15)"
        return True, tol, "Tolerancia válida"
    except (ValueError, TypeError):
        return False, 0, "La tolerancia debe ser un número"


def validar_iteraciones(max_iter: Union[int, str]) -> Tuple[bool, int, str]:
    """
    Valida que el número de iteraciones sea un entero positivo
    """
    try:
        max_iter = int(max_iter)
        if max_iter <= 0:
            return False, 0, "El número de iteraciones debe ser positivo"
        if max_iter > 10000:
            return False, 0, "El número de iteraciones es demasiado grande (máximo 10000)"
        return True, max_iter, "Número de iteraciones válido"
    except (ValueError, TypeError):
        return False, 0, "El número de iteraciones debe ser un entero"


def validar_valor_inicial(x0: Union[float, str], nombre: str = "x0") -> Tuple[bool, float, str]:
    """
    Valida que el valor inicial sea un número
    """
    try:
        x0 = float(x0)
        return True, x0, f"{nombre} válido"
    except (ValueError, TypeError):
        return False, 0, f"{nombre} debe ser un número"


def verificar_condiciones_punto_fijo(
    g: Callable[[float], float],
    g_derivada: Callable[[float], float],
    x0: float,
    intervalo: List[float] = None
) -> Dict:
    """
    Verifica condiciones de convergencia para punto fijo
    """
    from metodos.punto_fijo import verificar_condicion_convergencia
    
    if intervalo:
        resultado = verificar_condicion_convergencia(g_derivada, intervalo)
    else:
        # Verificar alrededor de x0
        intervalo_local = [x0 - 1, x0 + 1]
        resultado = verificar_condicion_convergencia(g_derivada, intervalo_local)
    
    # Verificar punto fijo aproximado
    g_x0 = g(x0)
    error_punto_fijo = abs(g_x0 - x0)
    
    resultado.update({
        'x0': x0,
        'g(x0)': g_x0,
        'error_punto_fijo_inicial': error_punto_fijo,
        'recomendacion': "Puede converger" if resultado['cumple_condicion'] and error_punto_fijo < 1 
                        else "Puede no converger"
    })
    
    return resultado


def formatear_numero(valor: float, decimales: int = 8, cientifico: bool = True) -> str:
    """
    Formatea números cumpliendo la especificación técnica:
    Mínimo 8 decimales y notación científica para valores pequeños o errores.
    """
    if valor is None or np.isnan(valor) or np.isinf(valor):
        return "N/A"
    
    # Obligar a notación científica para cumplir el requisito de "valores muy pequeños"
    return f"{valor:.{decimales}e}"