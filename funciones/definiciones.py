"""
Definiciones de funciones para los ejercicios prácticos
"""
import numpy as np
import sympy as sp

# Ejercicio 1: Optimización de Hash Table - Bisección
def T_lambda(lambd):
    """
    T(λ) = 2.5 + 0.8λ² - 3.2λ + ln(λ + 1)
    """
    return 2.5 + 0.8 * lambd**2 - 3.2 * lambd + np.log(lambd + 1)

def g_ejercicio1_convergente(lambd):
    """
    Despeje convergente para T(λ) = 0
    Se despeja λ del término lineal: 3.2λ = 2.5 + 0.8λ² + ln(λ + 1)
    """
    return (2.5 + 0.8 * lambd**2 + np.log(lambd + 1)) / 3.2

# Ejercicio 2: Balanceo de Carga - Falsa Posición
def E_workers(x):
    """
    E(x) = x³ - 6x² + 11x - 6.5
    """
    return x**3 - 6*x**2 + 11*x - 6.5

# Ejercicio 3: Crecimiento BD - Punto Fijo
def g_crecimiento(x):
    """
    x = 0.5cos(x) + 1.5
    """
    return 0.5 * np.cos(x) + 1.5

def g_crecimiento_derivada(x):
    """
    g'(x) = -0.5sen(x)
    """
    return -0.5 * np.sin(x)

# Ejercicio 4: Concurrencia - Newton-Raphson
def T_threads(n):
    """
    T(n) = n³ - 8n² + 20n - 16
    """
    return n**3 - 8*n**2 + 20*n - 16

def T_threads_derivada(n):
    """
    T'(n) = 3n² - 16n + 20
    """
    return 3*n**2 - 16*n + 20

# Ejercicio 5: Escalabilidad - Secante
def P_usuarios(x):
    """
    P(x) = x·e^(-x/2) - 0.3
    """
    return x * np.exp(-x/2) - 0.3

def P_usuarios_derivada(x):
    """
    P'(x) = e^(-x/2)(1 - x/2)
    """
    return np.exp(-x/2) * (1 - x/2)

# Diccionario de funciones para selección en interfaz
FUNCIONES = {
    "Ej1: Hash Table (Bisección)": {
        "funcion": T_lambda,
        "derivada": None,
        "intervalo": [0.5, 2.5],
        "x0": None,
        "g_convergente": g_ejercicio1_convergente,
        "descripcion": "T(λ) = 2.5 + 0.8λ² - 3.2λ + ln(λ + 1)",
        "interpretacion": "El valor λ encontrado es el factor de carga que minimiza el tiempo de búsqueda en el caché."
    },
    "Ej2: Balanceo (Falsa Posición)": {
        "funcion": E_workers,
        "derivada": None,
        "intervalo": [2, 4],
        "x0": None,
        "descripcion": "E(x) = x³ - 6x² + 11x - 6.5",
        "interpretacion": "El valor x representa el número óptimo de workers activos para balancear la carga del sistema distribuido."
    },
    "Ej3: Crecimiento BD (Punto Fijo)": {
        "funcion": g_crecimiento,
        "derivada": g_crecimiento_derivada,
        "x0": 1.0,
        "g_funcion": g_crecimiento,
        "descripcion": "x = 0.5cos(x) + 1.5",
        "interpretacion": "El valor x indica el número de meses desde el inicio en que la base de datos alcanzará el 80% de su capacidad."
    },
    "Ej4: Concurrencia (Newton)": {
        "funcion": T_threads,
        "derivada": T_threads_derivada,
        "x0": 3.0,
        "descripcion": "T(n) = n³ - 8n² + 20n - 16",
        "interpretacion": "El valor n es el número óptimo de threads donde el overhead de sincronización equilibra el beneficio del paralelismo."
    },
    "Ej5: Escalabilidad (Secante)": {
        "funcion": P_usuarios,
        "derivada": P_usuarios_derivada,
        "x0": 0.5,
        "x1": 1.0,
        "descripcion": "P(x) = x·e^(-x/2) - 0.3",
        "interpretacion": "El valor x (en miles de usuarios) representa el punto de equilibrio donde el costo de infraestructura iguala los ingresos."
    }
}
