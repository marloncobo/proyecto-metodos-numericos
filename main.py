#!/usr/bin/env python3
"""
Métodos Numéricos para Ingeniería de Software
Guía de Laboratorio - Corporación Universitaria Empresarial Alexander von Humboldt

Este programa implementa 5 métodos numéricos para resolver ecuaciones no lineales
con aplicaciones en Ingeniería de Software.
"""

import sys
import tkinter as tk
from interfaz.gui_principal import MetodosNumericosGUI


def main():
    """Función principal del programa"""
    print("=" * 60)
    print("MÉTODOS NUMÉRICOS PARA INGENIERÍA DE SOFTWARE")
    print("Resolución de Ecuaciones No Lineales")
    print("=" * 60)
    print("\nIniciando interfaz gráfica...")
    
    try:
        root = tk.Tk()
        app = MetodosNumericosGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("Por favor, verifique que todas las dependencias estén instaladas.")
        print("Ejecute: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()