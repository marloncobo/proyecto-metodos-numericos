# Métodos Numéricos para Ingeniería de Software

Implementación de 5 métodos numéricos para resolución de ecuaciones no lineales, aplicados a problemas reales de Ingeniería de Software.

## Estructura del Proyecto
- `metodos/`: Lógica matemática de los algoritmos numéricos.
- `interfaz/`: Interfaces gráficas usando Tkinter.
- `funciones/`: Modelos matemáticos de los ejercicios aplicados.
- `tests/`: Pruebas unitarias para validar la exactitud.

## Requisitos Previos
- Python 3.8 o superior.
- pip (gestor de paquetes de Python)

## Instalación y Ejecución
1. Clona el repositorio y navega a la carpeta del proyecto.
```bash
    git clone <url-del-repositorio>
    cd proyecto_metodos_numericos
```
2. Instala las dependencias necesarias:
```bash
    pip install -r requirements.txt
```

3. Ejecuta la interfaz gráfica principal:
```bash
    python main.py
```

3. Para ejecutar las pruebas unitarias:
```bash
    python -m unittest discover -s tests
```