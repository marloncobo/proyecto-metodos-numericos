"""
Interfaz gráfica principal usando tkinter y matplotlib
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

from funciones.definiciones import FUNCIONES
from metodos.biseccion import biseccion
from metodos.falsa_posicion import falsa_posicion, comparar_biseccion_falsa_posicion
from metodos.punto_fijo import punto_fijo, punto_fijo_multiple_inicial
from metodos.newton import newton_raphson, newton_multiple_inicial
from metodos.secante import secante, comparar_newton_secante
from utils.validaciones import *
from utils.parser import procesar_funcion_personalizada

# Colores y Estilos Globales
COLOR_BG = "#f4f6f9"        # Fondo general gris muy claro
COLOR_PANEL = "#ffffff"     # Fondo de paneles (blanco)
COLOR_ACCENT = "#3498db"    # Azul moderno
COLOR_TEXT = "#2c3e50"      # Gris oscuro para texto
FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_HEADER = ("Segoe UI", 12, "bold")
FONT_MATH = ("Consolas", 11, "bold")

class MetodosNumericosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos - Ingeniería de Software")
        self.root.geometry("1400x850")
        self.root.configure(bg=COLOR_BG)
        
        # Configurar estilos personalizados
        self.configurar_estilos()
        
        # Variable para método seleccionado
        self.metodo_actual = tk.StringVar(value="Bisección")
        
        self.crear_widgets()
        self.actualizar_campos_entrada()
    
    def configurar_estilos(self):
        """Configura el tema y estilos de los widgets"""
        style = ttk.Style()
        style.theme_use('clam')  # Base limpia
        
        # Configuración general
        style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT, font=FONT_MAIN)
        style.configure("TFrame", background=COLOR_BG)
        
        # Estilo para Paneles (Tarjetas blancas)
        style.configure("Card.TFrame", background=COLOR_PANEL, relief="flat")
        style.configure("Card.TLabel", background=COLOR_PANEL, font=FONT_MAIN)
        style.configure("Header.TLabel", background=COLOR_PANEL, font=FONT_HEADER, foreground=COLOR_ACCENT)
        
        # Estilo para Botones
        style.configure("Accent.TButton", 
                       font=FONT_BOLD, 
                       background=COLOR_ACCENT, 
                       foreground="white", 
                       borderwidth=0,
                       padding=10)
        style.map("Accent.TButton", 
                 background=[('active', '#2980b9'), ('pressed', '#1f618d')])
        
        style.configure("TButton", font=FONT_MAIN, padding=8)
        
        # Estilo para Entradas y Combobox
        style.configure("TEntry", padding=5, relief="flat", borderwidth=1)
        style.configure("TCombobox", padding=5)
        
        # Estilo para Treeview (Tabla)
        style.configure("Treeview", 
                       background="white",
                       fieldbackground="white",
                       foreground=COLOR_TEXT,
                       rowheight=30,
                       font=("Consolas", 9)) # Fuente monoespaciada para números
        
        style.configure("Treeview.Heading", 
                       font=FONT_BOLD, 
                       background="#ecf0f1", 
                       foreground=COLOR_TEXT,
                       relief="flat")
        
        style.map("Treeview", background=[('selected', COLOR_ACCENT)], foreground=[('selected', 'white')])
        
        # Estilo para Notebook (Pestañas)
        style.configure("TNotebook", background=COLOR_BG, tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab", padding=[15, 5], font=FONT_MAIN)
        style.map("TNotebook.Tab", background=[("selected", COLOR_PANEL)], expand=[("selected", [1, 1, 1, 0])])

    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # --- PANEL IZQUIERDO (CONTROLES) ---
        # Usamos un Frame con estilo "Card" para que parezca una tarjeta
        control_panel = ttk.Frame(main_frame, style="Card.TFrame", padding=20)
        control_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Título del panel
        ttk.Label(control_panel, text="Configuración", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Selección de método
        ttk.Label(control_panel, text="Método Numérico:", style="Card.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        metodos = ["Bisección", "Falsa Posición", "Punto Fijo", "Newton-Raphson", "Secante"]
        metodo_combo = ttk.Combobox(control_panel, textvariable=self.metodo_actual, 
                                   values=metodos, state="readonly", width=30)
        metodo_combo.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        metodo_combo.bind('<<ComboboxSelected>>', lambda e: self.actualizar_campos_entrada())
        
        # Selección de función
        ttk.Label(control_panel, text="Función a Resolver:", style="Card.TLabel").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.funcion_var = tk.StringVar()
        opciones_funciones = list(FUNCIONES.keys()) + ["Personalizada"]
        
        self.funciones_combo = ttk.Combobox(control_panel, textvariable=self.funcion_var,
                                      values=opciones_funciones, state="readonly", width=30)
        self.funciones_combo.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        self.funciones_combo.bind('<<ComboboxSelected>>', lambda e: self.mostrar_info_funcion())
        
        # Label para mostrar la ecuación
        self.lbl_ecuacion = ttk.Label(control_panel, text="", style="Card.TLabel", font=FONT_MATH, foreground=COLOR_ACCENT, wraplength=280)
        self.lbl_ecuacion.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        # Campo para función personalizada
        self.lbl_personalizada = ttk.Label(control_panel, text="Ecuación f(x):", style="Card.TLabel")
        self.entry_personalizada = ttk.Entry(control_panel)
        
        # Separador
        ttk.Separator(control_panel, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # Frame para campos dinámicos (a, b, x0, etc.)
        self.campos_frame = ttk.Frame(control_panel, style="Card.TFrame")
        self.campos_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Parámetros generales
        ttk.Label(control_panel, text="Parámetros de Ejecución:", style="Card.TLabel", font=FONT_BOLD).grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=(15, 10))
        
        # Tolerancia
        ttk.Label(control_panel, text="Tolerancia:", style="Card.TLabel").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.tolerancia_entry = ttk.Entry(control_panel, width=15)
        self.tolerancia_entry.grid(row=10, column=1, sticky=tk.E, pady=5)
        self.tolerancia_entry.insert(0, "1e-6")
        
        # Máx iteraciones
        ttk.Label(control_panel, text="Máx iteraciones:", style="Card.TLabel").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.max_iter_entry = ttk.Entry(control_panel, width=15)
        self.max_iter_entry.grid(row=11, column=1, sticky=tk.E, pady=5)
        self.max_iter_entry.insert(0, "100")
        
        # Tipo de error
        ttk.Label(control_panel, text="Tipo error:", style="Card.TLabel").grid(row=12, column=0, sticky=tk.W, pady=5)
        self.error_var = tk.StringVar(value="absoluto")
        error_combo = ttk.Combobox(control_panel, textvariable=self.error_var,
                                  values=["absoluto", "relativo"], state="readonly", width=13)
        error_combo.grid(row=12, column=1, sticky=tk.E, pady=5)
        
        # Botones de Acción
        botones_frame = ttk.Frame(control_panel, style="Card.TFrame")
        botones_frame.grid(row=13, column=0, columnspan=2, pady=30)
        
        ttk.Button(botones_frame, text="CALCULAR", style="Accent.TButton", command=self.calcular).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(botones_frame, text="Limpiar", command=self.limpiar).pack(side=tk.LEFT, padx=5)
        
        # --- PANEL DERECHO (RESULTADOS) ---
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestañas
        self.resultados_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        self.notebook.add(self.resultados_frame, text="  Resultados  ")
        
        self.graficas_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        self.notebook.add(self.graficas_frame, text="  Gráficas  ")
        
        self.comparacion_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        self.notebook.add(self.comparacion_frame, text="  Comparación  ")
        
        self.analisis_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        self.notebook.add(self.analisis_frame, text="  Análisis  ")
        
        # Configurar pesos del grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3) # El panel derecho es más ancho
        main_frame.rowconfigure(0, weight=1)
        control_panel.columnconfigure(1, weight=1)
    
    def actualizar_campos_entrada(self):
        """Actualiza los campos de entrada según el método seleccionado"""
        # Limpiar campos existentes
        for widget in self.campos_frame.winfo_children():
            widget.destroy()
        
        metodo = self.metodo_actual.get()
        
        # Helper para crear filas de entrada limpias
        def crear_fila(label_text, row):
            lbl = ttk.Label(self.campos_frame, text=label_text, style="Card.TLabel")
            lbl.grid(row=row, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(self.campos_frame, width=15)
            entry.grid(row=row, column=1, sticky=tk.E, pady=5)
            return entry

        if metodo == "Bisección" or metodo == "Falsa Posición":
            self.a_entry = crear_fila("Límite inferior (a):", 0)
            self.b_entry = crear_fila("Límite superior (b):", 1)
            
            if self.funcion_var.get() and self.funcion_var.get() != "Personalizada":
                func_info = FUNCIONES[self.funcion_var.get()]
                if 'intervalo' in func_info:
                    self.a_entry.insert(0, str(func_info['intervalo'][0]))
                    self.b_entry.insert(0, str(func_info['intervalo'][1]))
        
        elif metodo == "Punto Fijo":
            self.x0_entry = crear_fila("Valor inicial (x0):", 0)
            
            if self.funcion_var.get() and self.funcion_var.get() != "Personalizada":
                func_info = FUNCIONES[self.funcion_var.get()]
                if 'x0' in func_info:
                    self.x0_entry.insert(0, str(func_info['x0']))
        
        elif metodo == "Newton-Raphson":
            self.x0_entry = crear_fila("Valor inicial (x0):", 0)
            
            if self.funcion_var.get() and self.funcion_var.get() != "Personalizada":
                func_info = FUNCIONES[self.funcion_var.get()]
                if 'x0' in func_info:
                    self.x0_entry.insert(0, str(func_info['x0']))
        
        elif metodo == "Secante":
            self.x0_entry = crear_fila("Valor inicial (x0):", 0)
            self.x1_entry = crear_fila("Valor inicial (x1):", 1)
            
            if self.funcion_var.get() and self.funcion_var.get() != "Personalizada":
                func_info = FUNCIONES[self.funcion_var.get()]
                if 'x0' in func_info:
                    self.x0_entry.insert(0, str(func_info['x0']))
                if 'x1' in func_info:
                    self.x1_entry.insert(0, str(func_info['x1']))
    
    def mostrar_info_funcion(self):
        """Muestra información de la función seleccionada o habilita campo personalizada"""
        seleccion = self.funcion_var.get()
        
        if seleccion == "Personalizada":
            self.lbl_personalizada.grid(row=6, column=0, sticky=tk.W, pady=5)
            self.entry_personalizada.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
            self.lbl_ecuacion.config(text="") # Limpiar label de ecuación
            
            # Mostrar ayuda solo la primera vez o si está vacío
            if not self.entry_personalizada.get():
                pass # Opcional: mostrar tooltip
        else:
            self.lbl_personalizada.grid_remove()
            self.entry_personalizada.grid_remove()
            
            if seleccion:
                func_info = FUNCIONES[seleccion]
                # Actualizar el label con la descripción de la función
                self.lbl_ecuacion.config(text=func_info['descripcion'])
        
        self.actualizar_campos_entrada()
    
    def calcular(self):
        """Ejecuta el método numérico seleccionado"""
        try:
            seleccion_func = self.funcion_var.get()
            if not seleccion_func:
                messagebox.showerror("Error", "Seleccione una función")
                return
            
            tol_valida, tol, msg_tol = validar_tolerancia(self.tolerancia_entry.get())
            if not tol_valida:
                messagebox.showerror("Error", msg_tol)
                return
            
            iter_valida, max_iter, msg_iter = validar_iteraciones(self.max_iter_entry.get())
            if not iter_valida:
                messagebox.showerror("Error", msg_iter)
                return
            
            if seleccion_func == "Personalizada":
                texto_func = self.entry_personalizada.get()
                if not texto_func:
                    messagebox.showerror("Error", "Ingrese la ecuación de la función personalizada")
                    return
                
                f, f_derivada, texto_derivada, error = procesar_funcion_personalizada(texto_func)
                if error:
                    messagebox.showerror("Error en función", error)
                    return
                
                func_info = {
                    'funcion': f,
                    'derivada': f_derivada,
                    'descripcion': f"f(x) = {texto_func}",
                    'g_funcion': f,
                    'interpretacion': "Función personalizada definida por el usuario."
                }
            else:
                func_info = FUNCIONES[seleccion_func]
                f = func_info['funcion']
            
            metodo = self.metodo_actual.get()
            self.limpiar_pestanas()
            
            if metodo == "Bisección":
                self.ejecutar_biseccion(f, tol, max_iter, func_info)
            elif metodo == "Falsa Posición":
                self.ejecutar_falsa_posicion(f, tol, max_iter, func_info)
            elif metodo == "Punto Fijo":
                if seleccion_func == "Personalizada":
                    messagebox.showinfo("Aviso", "Para Punto Fijo personalizada, asegúrese de haber ingresado g(x) tal que x = g(x)")
                self.ejecutar_punto_fijo(func_info, tol, max_iter)
            elif metodo == "Newton-Raphson":
                self.ejecutar_newton(func_info, tol, max_iter)
            elif metodo == "Secante":
                self.ejecutar_secante(func_info, tol, max_iter)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la ejecución: {str(e)}")
    
    # --- MÉTODOS DE EJECUCIÓN ---
    
    def ejecutar_biseccion(self, f, tol, max_iter, func_info):
        a_valida, a, _ = validar_valor_inicial(self.a_entry.get(), "a")
        b_valida, b, _ = validar_valor_inicial(self.b_entry.get(), "b")
        
        if not a_valida or not b_valida:
            messagebox.showerror("Error", "Valores de intervalo inválidos")
            return
        
        valido, msg = validar_intervalo_raiz(f, a, b)
        if not valido:
            messagebox.showerror("Error de Dominio/Intervalo", msg)
            return
        
        resultado = biseccion(f, a, b, tol, max_iter, self.error_var.get())
        self.mostrar_resultados_biseccion(resultado)
        self.graficar_biseccion(f, a, b, resultado)
        self._mostrar_analisis(resultado, func_info)
        
        if messagebox.askyesno("Comparar", "¿Comparar con método de Falsa Posición?"):
            self.comparar_biseccion_falsa(f, a, b, tol, max_iter)
    
    def ejecutar_falsa_posicion(self, f, tol, max_iter, func_info):
        a_valida, a, _ = validar_valor_inicial(self.a_entry.get(), "a")
        b_valida, b, _ = validar_valor_inicial(self.b_entry.get(), "b")
        
        if not a_valida or not b_valida:
            messagebox.showerror("Error", "Valores de intervalo inválidos")
            return
        
        valido, msg = validar_intervalo_raiz(f, a, b)
        if not valido:
            messagebox.showerror("Error de Dominio/Intervalo", msg)
            return
        
        resultado = falsa_posicion(f, a, b, tol, max_iter, self.error_var.get())
        self.mostrar_resultados_falsa_posicion(resultado)
        self.graficar_falsa_posicion(f, a, b, resultado)
        self._mostrar_analisis(resultado, func_info)
        
        # --- AÑADIDO: Comparación con Bisección ---
        if messagebox.askyesno("Comparar", "¿Comparar con método de Bisección?"):
            self.comparar_biseccion_falsa(f, a, b, tol, max_iter)
    
    def ejecutar_punto_fijo(self, func_info, tol, max_iter):
        x0_valida, x0, _ = validar_valor_inicial(self.x0_entry.get(), "x0")
        if not x0_valida:
            messagebox.showerror("Error", "Valor inicial inválido")
            return
        
        if 'g_convergente' in func_info:
            g = func_info['g_convergente']
        elif 'g_funcion' in func_info:
            g = func_info['g_funcion']
        else:
            g = func_info['funcion']

        g_derivada = func_info.get('derivada')
        if g_derivada:
            condicion = verificar_condiciones_punto_fijo(g, g_derivada, x0)
            if not condicion['cumple_condicion']:
                messagebox.showwarning("Advertencia", f"|g'(x)| máxima: {condicion['max_g_prime']:.4f}\nEl método puede no converger")
        
        resultado = punto_fijo(g, x0, tol, max_iter, g_derivada)
        self.mostrar_resultados_punto_fijo(resultado)
        self.graficar_punto_fijo(g, x0, resultado)
        self._mostrar_analisis(resultado, func_info)
        
        # --- AÑADIDO: Análisis de Sensibilidad (Ejercicio 3) ---
        if messagebox.askyesno("Análisis de Sensibilidad", "¿Desea comparar diferentes valores iniciales (0.5, 1.0, 1.5, 2.0)?"):
            self.comparar_punto_fijo_ui(g, g_derivada, tol)
    
    def ejecutar_newton(self, func_info, tol, max_iter):
        x0_valida, x0, _ = validar_valor_inicial(self.x0_entry.get(), "x0")
        if not x0_valida:
            messagebox.showerror("Error", "Valor inicial inválido")
            return
        
        f = func_info['funcion']
        f_derivada = func_info.get('derivada')
        if f_derivada is None:
            messagebox.showerror("Error", "Esta función no tiene derivada definida")
            return
        
        resultado = newton_raphson(f, f_derivada, x0, tol, max_iter, self.error_var.get())
        self.mostrar_resultados_newton(resultado)
        self.graficar_newton(f, x0, resultado)
        self._mostrar_analisis(resultado, func_info)
        
        # --- AÑADIDO: Análisis de Sensibilidad (Ejercicio 4) ---
        if messagebox.askyesno("Análisis de Sensibilidad", "¿Desea comparar diferentes valores iniciales (1.0, 2.0, 3.0, 5.0)?"):
            self.comparar_newton_iniciales_ui(f, f_derivada, tol)
        
        # --- AÑADIDO: Comparación con Secante ---
        elif messagebox.askyesno("Comparar", "¿Comparar con método de la Secante?"):
            # Asumimos un x1 cercano para la secante ya que no se pide en la entrada de Newton
            x1_estimado = x0 + 0.1
            self.comparar_newton_secante_ui(f, f_derivada, x0, x0, x1_estimado, tol)
    
    def ejecutar_secante(self, func_info, tol, max_iter):
        x0_valida, x0, _ = validar_valor_inicial(self.x0_entry.get(), "x0")
        x1_valida, x1, _ = validar_valor_inicial(self.x1_entry.get(), "x1")
        if not x0_valida or not x1_valida:
            messagebox.showerror("Error", "Valores iniciales inválidos")
            return
        
        f = func_info['funcion']
        resultado = secante(f, x0, x1, tol, max_iter, self.error_var.get())
        self.mostrar_resultados_secante(resultado)
        self.graficar_secante(f, x0, x1, resultado)
        self._mostrar_analisis(resultado, func_info)
        
        f_derivada = func_info.get('derivada')
        if f_derivada and messagebox.askyesno("Comparar", "¿Comparar con método de Newton-Raphson?"):
            self.comparar_newton_secante_ui(f, f_derivada, x0, x0, x1, tol)
    
    # --- MÉTODOS DE VISUALIZACIÓN (Estilizados) ---
    
    def _crear_tabla(self, columns):
        """Helper para crear tablas estilizadas"""
        frame = ttk.Frame(self.resultados_frame, style="Card.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Configurar tags para filas alternas
        tree.tag_configure('odd', background='#f8f9fa')
        tree.tag_configure('even', background='#ffffff')
        
        return tree

    def _mostrar_resumen(self, resultado, extra_info=None):
        """Muestra el panel de resumen estilizado"""
        resumen_frame = ttk.LabelFrame(self.resultados_frame, text="Resumen de Ejecución", padding=15)
        resumen_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=10)
        
        # Grid para organizar info
        grid_frame = ttk.Frame(resumen_frame)
        grid_frame.pack(fill=tk.X)
        
        def add_item(label, value, row, col):
            ttk.Label(grid_frame, text=label, font=FONT_BOLD).grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            ttk.Label(grid_frame, text=value).grid(row=row, column=col+1, sticky=tk.W, padx=5, pady=2)

        raiz_txt = f"{resultado['raiz']:.10f}" if resultado['raiz'] is not None else "No encontrada"
        add_item("Raíz encontrada:", raiz_txt, 0, 0)
        add_item("Iteraciones:", str(resultado['iteraciones_totales']), 1, 0)
        add_item("Error final:", f"{resultado['error_final']:.2e}", 0, 2)
        add_item("Tiempo:", f"{resultado['tiempo_ejecucion']:.4f} s", 1, 2)
        
        status_color = "green" if resultado['convergio'] else "red"
        status_txt = "Convergencia Exitosa" if resultado['convergio'] else "No Convergió"
        lbl_status = ttk.Label(resumen_frame, text=status_txt, foreground=status_color, font=FONT_BOLD)
        lbl_status.pack(anchor=tk.E, pady=5)
        
        if extra_info:
            ttk.Label(resumen_frame, text=extra_info, foreground="gray", wraplength=800).pack(anchor=tk.W, pady=5)

    def _mostrar_analisis(self, resultado, func_info):
        """Muestra la interpretación y análisis del resultado"""
        # Limpiar frame
        for widget in self.analisis_frame.winfo_children():
            widget.destroy()
            
        # Contenedor principal
        container = ttk.Frame(self.analisis_frame, style="Card.TFrame", padding=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(container, text="Análisis del Problema", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 15))
        
        # Contexto del Problema
        ttk.Label(container, text="Contexto:", font=FONT_BOLD).pack(anchor=tk.W, pady=(5, 2))
        interpretacion = func_info.get('interpretacion', "No hay información de contexto disponible para esta función.")
        
        # Usar Text widget para texto multilínea con wrap
        txt_contexto = tk.Text(container, height=4, wrap=tk.WORD, font=FONT_MAIN, 
                              bg=COLOR_BG, relief="flat", padx=10, pady=10)
        txt_contexto.insert(tk.END, interpretacion)
        txt_contexto.config(state=tk.DISABLED) # Solo lectura
        txt_contexto.pack(fill=tk.X, pady=(0, 15))
        
        # Conclusión basada en resultados
        ttk.Label(container, text="Conclusión:", font=FONT_BOLD).pack(anchor=tk.W, pady=(5, 2))
        
        conclusion = ""
        if resultado['convergio'] and resultado['raiz'] is not None:
            raiz = resultado['raiz']
            
            # Generar conclusión específica según el ejercicio
            nombre_func = self.funcion_var.get()
            
            if "Ej1" in nombre_func:
                conclusion = f"El valor encontrado de λ ≈ {raiz:.6f} representa el factor de carga óptimo según el modelo matemático. En ese punto, el comportamiento del tiempo de búsqueda alcanza el equilibrio definido por la función, lo que permite estimar la configuración más eficiente del sistema de caché."
            
            elif "Ej2" in nombre_func:
                conclusion = f"El valor encontrado x ≈ {raiz:.6f} representa el número óptimo de workers activos según el modelo de eficiencia. En ese punto, el sistema alcanza un equilibrio entre carga y capacidad de procesamiento."
            
            elif "Ej3" in nombre_func:
                conclusion = f"El valor obtenido x ≈ {raiz:.6f} representa el número de meses necesarios para que la base de datos alcance el 80% de su capacidad según el modelo de crecimiento. Este resultado permite planificar ampliaciones o limpieza de datos."
            
            elif "Ej4" in nombre_func:
                conclusion = f"El valor encontrado n ≈ {raiz:.6f} representa el número de threads donde, según el modelo, el beneficio del paralelismo se equilibra con el costo de sincronización. Este punto permite estimar una configuración eficiente del sistema paralelo."
            
            elif "Ej5" in nombre_func:
                conclusion = f"El valor encontrado x ≈ {raiz:.6f} representa el número de miles de usuarios activos necesarios para que los ingresos igualen los costos de infraestructura. A partir de ese punto, la plataforma comienza a ser rentable."
            
            else:
                # Caso genérico o personalizada
                conclusion = f"El método convergió exitosamente a la solución x ≈ {raiz:.6f}.\n\n"
                conclusion += f"Esto significa que, bajo las condiciones dadas, el valor que satisface la ecuación es {raiz:.6f}."
                
        else:
            conclusion = "El método no logró converger a una solución válida dentro de los parámetros establecidos.\n"
            conclusion += "Se recomienda revisar los valores iniciales o aumentar el número de iteraciones."
            
        txt_conclusion = tk.Text(container, height=6, wrap=tk.WORD, font=FONT_MAIN,
                                bg=COLOR_BG, relief="flat", padx=10, pady=10)
        txt_conclusion.insert(tk.END, conclusion)
        txt_conclusion.config(state=tk.DISABLED)
        txt_conclusion.pack(fill=tk.X)

    def mostrar_resultados_biseccion(self, resultado):
        self._mostrar_resumen(resultado)
        
        columns = ('n', 'a', 'b', 'c', 'f(c)', 'error_abs', 'error_rel')
        tree = self._crear_tabla(columns)
        
        headers = ['Iter', 'a', 'b', 'c', 'f(c)', 'Error Abs', 'Error Rel']
        for col, h in zip(columns, headers):
            tree.heading(col, text=h)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        for i, it in enumerate(resultado['iteraciones']):
            tag = 'even' if i % 2 == 0 else 'odd'
            tree.insert('', tk.END, values=(
                it['n'],
                f"{it['a']:.8f}", f"{it['b']:.8f}", f"{it['c']:.8f}",
                f"{it['f(c)']:.8e}", f"{it['error_abs']:.8e}", f"{it['error_rel']:.8e}"
            ), tags=(tag,))

    def mostrar_resultados_falsa_posicion(self, resultado):
        self._mostrar_resumen(resultado)
        
        columns = ('n', 'a', 'b', 'c', 'f(c)', 'error_abs', 'error_rel')
        tree = self._crear_tabla(columns)
        
        headers = ['Iter', 'a', 'b', 'c', 'f(c)', 'Error Abs', 'Error Rel']
        for col, h in zip(columns, headers):
            tree.heading(col, text=h)
            tree.column(col, width=100, anchor=tk.CENTER)
            
        for i, it in enumerate(resultado['iteraciones']):
            tag = 'even' if i % 2 == 0 else 'odd'
            tree.insert('', tk.END, values=(
                it['n'],
                f"{it['a']:.8f}", f"{it['b']:.8f}", f"{it['c']:.8f}",
                f"{it['f(c)']:.8e}", f"{it['error_abs']:.8e}", f"{it['error_rel']:.8e}"
            ), tags=(tag,))

    def mostrar_resultados_punto_fijo(self, resultado):
        self._mostrar_resumen(resultado, resultado.get('mensaje', ''))
        
        columns = ('n', 'x_n', 'g(x_n)', 'diferencia', 'error_abs', 'error_rel')
        tree = self._crear_tabla(columns)
        
        headers = ['Iter', 'x_n', 'g(x_n)', '|x_n - g(x_n)|', 'Error Abs', 'Error Rel']
        for col, h in zip(columns, headers):
            tree.heading(col, text=h)
            tree.column(col, width=110, anchor=tk.CENTER)
            
        for i, it in enumerate(resultado['iteraciones']):
            tag = 'even' if i % 2 == 0 else 'odd'
            tree.insert('', tk.END, values=(
                it['n'],
                f"{it['x_n']:.8f}", f"{it['g(x_n)']:.8f}",
                f"{it['diferencia']:.8e}", f"{it['error_abs']:.8e}", f"{it['error_rel']:.8e}"
            ), tags=(tag,))

    def mostrar_resultados_newton(self, resultado):
        extra = ""
        if 'convergencia_cuadratica' in resultado:
            cc = resultado['convergencia_cuadratica']
            extra = "✓ Convergencia cuadrática verificada" if cc.get('es_cuadratica', False) else "✗ No se observa convergencia cuadrática"
        self._mostrar_resumen(resultado, extra)
        
        columns = ('n', 'x_n', 'f(x_n)', "f'(x_n)", 'x_next', 'error_abs', 'error_rel')
        tree = self._crear_tabla(columns)
        
        headers = ['Iter', 'x_n', 'f(x_n)', "f'(x_n)", 'x_{n+1}', 'Error Abs', 'Error Rel']
        for col, h in zip(columns, headers):
            tree.heading(col, text=h)
            tree.column(col, width=100, anchor=tk.CENTER)
            
        for i, it in enumerate(resultado['iteraciones']):
            tag = 'even' if i % 2 == 0 else 'odd'
            f_prime = it["f'(x_n)"]
            tree.insert('', tk.END, values=(
                it['n'],
                f"{it['x_n']:.10f}", f"{it['f(x_n)']:.8e}", f"{f_prime:.8f}",
                f"{it['x_next']:.10f}", f"{it['error_abs']:.8e}", f"{it['error_rel']:.8e}"
            ), tags=(tag,))

    def mostrar_resultados_secante(self, resultado):
        self._mostrar_resumen(resultado, f"Evaluaciones de función: {resultado.get('evaluaciones_funcion', 0)}")
        
        columns = ('n', 'x_{n-1}', 'x_n', 'f(x_{n-1})', 'f(x_n)', 'x_{n+1}', 'error_abs', 'error_rel')
        tree = self._crear_tabla(columns)
        
        headers = ['Iter', 'x_{n-1}', 'x_n', 'f(x_{n-1})', 'f(x_n)', 'x_{n+1}', 'Error Abs', 'Error Rel']
        for col, h in zip(columns, headers):
            tree.heading(col, text=h)
            tree.column(col, width=90, anchor=tk.CENTER)
            
        for i, it in enumerate(resultado['iteraciones']):
            tag = 'even' if i % 2 == 0 else 'odd'
            tree.insert('', tk.END, values=(
                it['n'],
                f"{it['x_{n-1}']:.9f}", f"{it['x_n']:.9f}",
                f"{it['f(x_{n-1})']:.8e}", f"{it['f(x_n)']:.8e}",
                f"{it['x_{n+1}']:.9f}", f"{it['error_abs']:.8e}", f"{it['error_rel']:.8e}"
            ), tags=(tag,))

    # --- GRÁFICAS (Ajustes estéticos) ---
    
    def _configurar_grafica(self, fig, ax_list):
        """Aplica estilo consistente a las gráficas"""
        fig.patch.set_facecolor('white')
        for ax in ax_list:
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # --- NUEVO: Ejes más marcados ---
            ax.axhline(0, color='black', linewidth=1.5, alpha=0.8)
            ax.axvline(0, color='black', linewidth=1.5, alpha=0.8)
            # --------------------------------

    def _agregar_tooltip(self, fig, ax, artist, labels_func):
        """
        Agrega un tooltip interactivo a un elemento de la gráfica (scatter o line).
        
        Args:
            fig: La figura de matplotlib.
            ax: El eje donde está el artista.
            artist: El objeto (PathCollection para scatter) que dispara el evento.
            labels_func: Función que recibe el índice del punto y devuelve el texto a mostrar.
        """
        annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(ind):
            # Obtener posición del punto
            pos = artist.get_offsets()[ind["ind"][0]]
            annot.xy = pos
            
            # Obtener texto usando la función proporcionada
            idx = ind["ind"][0]
            text = labels_func(idx)
            
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.9)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                cont, ind = artist.contains(event)
                if cont:
                    update_annot(ind)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)
        
    def _graficar_error_log(self, fig, ax, errores, color='#27ae60', label=None, marker='o'):
        """
        Función auxiliar robusta para graficar errores en escala logarítmica.
        Maneja automáticamente valores <= 0 reemplazándolos por epsilon.
        """
        if not errores:
            return None
            
        # Limpieza robusta de datos: reemplazar <= 0 por 1e-20
        errores_limpios = [max(float(e), 1e-20) if not np.isnan(e) and not np.isinf(e) else 1e-20 for e in errores]
        iteraciones = range(1, len(errores_limpios) + 1)
        
        # Graficar línea
        ax.semilogy(iteraciones, errores_limpios, color=color, linestyle='-', linewidth=1, label=label)
        
        # Graficar puntos (para tooltips)
        sc = ax.scatter(iteraciones, errores_limpios, color=color, s=15, marker=marker)
        
        return sc

    def graficar_biseccion(self, f, a, b, resultado):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=100)
        self._configurar_grafica(fig, [ax1, ax2])
        
        # Filtrar dominio para evitar errores de logaritmo en la gráfica de función
        x = np.linspace(a - 0.5, b + 0.5, 1000)
        y = []
        x_validos = []
        for xi in x:
            try:
                val = f(xi)
                if not np.isnan(val) and not np.isinf(val):
                    y.append(val)
                    x_validos.append(xi)
            except:
                pass
        
        ax1.plot(x_validos, y, color=COLOR_ACCENT, label='f(x)', linewidth=2)
        
        # --- NUEVO: Resaltado de Raíz ---
        ax1.plot(resultado['raiz'], 0, 'o', color='#f1c40f', markersize=10, markeredgecolor='black', zorder=10, label='Raíz')
        ax1.annotate('Raíz', xy=(resultado['raiz'], 0), xytext=(10, 10), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
        # --------------------------------
        
        # --- NUEVO: Líneas de Iteración (Intervalos) ---
        # Mostramos solo las primeras 5 y la última para no saturar
        iters_to_show = resultado['iteraciones'][:5]
        if len(resultado['iteraciones']) > 5:
            iters_to_show.append(resultado['iteraciones'][-1])
            
        for it in iters_to_show:
            ax1.axvline(x=it['a'], color='gray', linestyle=':', alpha=0.3)
            ax1.axvline(x=it['b'], color='gray', linestyle=':', alpha=0.3)
        # -----------------------------------------------
        
        xs = [it['c'] for it in resultado['iteraciones']]
        ys = [it['f(c)'] for it in resultado['iteraciones']]
        sc1 = ax1.scatter(xs, ys, color='#e74c3c', s=20, zorder=5)
        
        # Tooltip para gráfica de función
        self._agregar_tooltip(fig, ax1, sc1, lambda i: f"Iter: {resultado['iteraciones'][i]['n']}\nx: {xs[i]:.6f}\ny: {ys[i]:.2e}")
        
        ax1.set_title('Convergencia de Raíz')
        ax1.legend()
        
        errores = [it['error_abs'] for it in resultado['iteraciones']]
        sc2 = self._graficar_error_log(fig, ax2, errores)
        
        # Tooltip para gráfica de error
        if sc2:
            self._agregar_tooltip(fig, ax2, sc2, lambda i: f"Iter: {i+1}\nError: {errores[i]:.2e}")

        ax2.set_title('Evolución del Error')
        ax2.set_xlabel('Iteración')
        
        plt.tight_layout()
        self._mostrar_canvas(fig, self.graficas_frame)

    def graficar_falsa_posicion(self, f, a, b, resultado):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=100)
        self._configurar_grafica(fig, [ax1, ax2])
        
        x = np.linspace(a - 0.5, b + 0.5, 1000)
        y = [f(xi) for xi in x]
        
        ax1.plot(x, y, color=COLOR_ACCENT, linewidth=2, label='f(x)')
        
        # --- NUEVO: Resaltado de Raíz ---
        ax1.plot(resultado['raiz'], 0, 'o', color='#f1c40f', markersize=10, markeredgecolor='black', zorder=10, label='Raíz')
        ax1.annotate('Raíz', xy=(resultado['raiz'], 0), xytext=(10, 10), textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
        # --------------------------------
        
        # --- NUEVO: Líneas de Iteración (Cuerdas) ---
        # Mostrar TODAS las iteraciones pero muy tenues
        for it in resultado['iteraciones']:
            # Línea entre (a, f(a)) y (b, f(b))
            ax1.plot([it['a'], it['b']], [it['f(a)'], it['f(b)']], color='gray', linestyle='--', alpha=0.2)
        # --------------------------------------------
        
        xs = [it['c'] for it in resultado['iteraciones']]
        ys = [f(xi) for xi in xs]
        sc1 = ax1.scatter(xs, ys, color='#e74c3c', s=20, label='Iteraciones')
        
        self._agregar_tooltip(fig, ax1, sc1, lambda i: f"Iter: {resultado['iteraciones'][i]['n']}\nx: {xs[i]:.6f}\ny: {ys[i]:.2e}")
        
        ax1.set_title('Falsa Posición')
        ax1.legend()
        
        errores = [it['error_abs'] for it in resultado['iteraciones']]
        sc2 = self._graficar_error_log(fig, ax2, errores)
        
        if sc2:
            self._agregar_tooltip(fig, ax2, sc2, lambda i: f"Iter: {i+1}\nError: {errores[i]:.2e}")
        
        ax2.set_title('Error Absoluto')
        
        plt.tight_layout()
        self._mostrar_canvas(fig, self.graficas_frame)

    def graficar_punto_fijo(self, g, x0, resultado):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=100)
        self._configurar_grafica(fig, [ax1, ax2])
        
        raiz_val = resultado['raiz'] if resultado['raiz'] is not None else x0
        x_min = min(0, x0 - 1, raiz_val - 1)
        x_max = max(2, x0 + 1, raiz_val + 1)
        x = np.linspace(x_min, x_max, 1000)
        y_g = [g(xi) for xi in x]
        
        ax1.plot(x, x, 'k--', label='y = x', alpha=0.5)
        ax1.plot(x, y_g, color=COLOR_ACCENT, label='y = g(x)', linewidth=2)
        
        # --- NUEVO: Resaltado de Raíz ---
        if resultado['raiz']:
            ax1.plot(resultado['raiz'], resultado['raiz'], 'o', color='#f1c40f', markersize=10, markeredgecolor='black', zorder=10, label='Raíz')
        # --------------------------------
        
        if resultado['iteraciones']:
            xs = [it['x_n'] for it in resultado['iteraciones']]
            xs.append(resultado['iteraciones'][-1]['g(x_n)'])
            for i in range(len(xs) - 1):
                ax1.plot([xs[i], xs[i]], [xs[i], xs[i+1]], color='#e74c3c', alpha=0.4, linewidth=1)
                ax1.plot([xs[i], xs[i+1]], [xs[i+1], xs[i+1]], color='#e74c3c', alpha=0.4, linewidth=1)
            
            # Puntos para tooltip (solo los x_n sobre la curva g(x))
            sc1 = ax1.scatter(xs[:-1], [g(xi) for xi in xs[:-1]], color='#e74c3c', s=20, zorder=5, label='Iteraciones')
            self._agregar_tooltip(fig, ax1, sc1, lambda i: f"Iter: {i+1}\nx: {xs[i]:.6f}\ng(x): {g(xs[i]):.6f}")

        ax1.set_title('Diagrama de Telaraña')
        ax1.legend()
        
        if resultado['iteraciones']:
            errores = [it['error_abs'] for it in resultado['iteraciones']]
            sc2 = self._graficar_error_log(fig, ax2, errores)
            if sc2:
                self._agregar_tooltip(fig, ax2, sc2, lambda i: f"Iter: {i+1}\nError: {errores[i]:.2e}")
            
            ax2.set_title('Error Absoluto')
        
        plt.tight_layout()
        self._mostrar_canvas(fig, self.graficas_frame)

    def graficar_newton(self, f, x0, resultado):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=100)
        self._configurar_grafica(fig, [ax1, ax2])
        
        raiz_val = resultado['raiz'] if resultado['raiz'] is not None else x0
        x_min = min(x0 - 2, raiz_val - 1)
        x_max = max(x0 + 2, raiz_val + 1)
        x = np.linspace(x_min, x_max, 1000)
        y = [f(xi) for xi in x]
        
        ax1.plot(x, y, color=COLOR_ACCENT, linewidth=2, label='f(x)')
        
        # --- NUEVO: Resaltado de Raíz ---
        if resultado['raiz']:
            ax1.plot(resultado['raiz'], 0, 'o', color='#f1c40f', markersize=10, markeredgecolor='black', zorder=10, label='Raíz')
        # --------------------------------
        
        # Tangentes (solo últimas 5 para no saturar)
        iteraciones = resultado['iteraciones']
        start_idx = max(0, len(iteraciones) - 5)
        for i in range(start_idx, len(iteraciones) - 1):
            it = iteraciones[i]
            x_n = it['x_n']
            f_n = it['f(x_n)']
            f_prime = it["f'(x_n)"]
            x_tang = np.linspace(x_n - 0.5, x_n + 0.5, 10)
            y_tang = f_n + f_prime * (x_tang - x_n)
            ax1.plot(x_tang, y_tang, color='#95a5a6', linestyle='--', alpha=0.5)
            
        # Puntos de iteración
        xs = [it['x_n'] for it in iteraciones]
        ys = [it['f(x_n)'] for it in iteraciones]
        sc1 = ax1.scatter(xs, ys, color='#e74c3c', s=20, zorder=5, label='Iteraciones')
        self._agregar_tooltip(fig, ax1, sc1, lambda i: f"Iter: {iteraciones[i]['n']}\nx: {xs[i]:.6f}\nf(x): {ys[i]:.2e}")

        ax1.set_title('Newton-Raphson')
        ax1.legend()
        
        errores = [it['error_abs'] for it in resultado['iteraciones']]
        sc2 = self._graficar_error_log(fig, ax2, errores)
        if sc2:
            self._agregar_tooltip(fig, ax2, sc2, lambda i: f"Iter: {i+1}\nError: {errores[i]:.2e}")
        
        ax2.set_title('Error Absoluto')
        
        plt.tight_layout()
        self._mostrar_canvas(fig, self.graficas_frame)

    def graficar_secante(self, f, x0, x1, resultado):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=100)
        self._configurar_grafica(fig, [ax1, ax2])
        
        raiz_val = resultado['raiz'] if resultado['raiz'] is not None else x1
        x_min = min(x0, x1, raiz_val) - 1
        x_max = max(x0, x1, raiz_val) + 1
        x = np.linspace(x_min, x_max, 1000)
        y = [f(xi) for xi in x]
        
        ax1.plot(x, y, color=COLOR_ACCENT, linewidth=2, label='f(x)')
        
        # --- NUEVO: Resaltado de Raíz ---
        if resultado['raiz']:
            ax1.plot(resultado['raiz'], 0, 'o', color='#f1c40f', markersize=10, markeredgecolor='black', zorder=10, label='Raíz')
        # --------------------------------
        
        # Dibujar secantes
        iteraciones = resultado['iteraciones']
        # Mostrar solo las últimas 5 para no saturar si hay muchas
        start_idx = max(0, len(iteraciones) - 5)
        
        for i in range(start_idx, len(iteraciones) - 1):
            it = iteraciones[i]
            x_prev = it['x_{n-1}']
            x_curr = it['x_n']
            f_prev = it['f(x_{n-1})']
            f_curr = it['f(x_n)']
            
            # Recta secante que pasa por (x_prev, f_prev) y (x_curr, f_curr)
            # Extendemos un poco la línea para visualizarla mejor
            x_sec = np.linspace(min(x_prev, x_curr) - 0.5, max(x_prev, x_curr) + 0.5, 10)
            
            if abs(x_curr - x_prev) > 1e-10:
                pendiente = (f_curr - f_prev) / (x_curr - x_prev)
                y_sec = f_prev + pendiente * (x_sec - x_prev)
                ax1.plot(x_sec, y_sec, color='#95a5a6', linestyle='--', alpha=0.5)
                
                # Marcar los puntos usados para la secante
                ax1.scatter([x_prev, x_curr], [f_prev, f_curr], color='#e74c3c', s=10, zorder=3)

        # Puntos de iteración (nuevos x)
        xs = [it['x_n'] for it in iteraciones]
        ys = [it['f(x_n)'] for it in iteraciones]
        sc1 = ax1.scatter(xs, ys, color='#e74c3c', s=20, zorder=5, label='Iteraciones')
        self._agregar_tooltip(fig, ax1, sc1, lambda i: f"Iter: {iteraciones[i]['n']}\nx: {xs[i]:.6f}\nf(x): {ys[i]:.2e}")

        ax1.set_title('Método de la Secante')
        ax1.legend()
        
        errores = [it['error_abs'] for it in resultado['iteraciones']]
        sc2 = self._graficar_error_log(fig, ax2, errores)
        if sc2:
            self._agregar_tooltip(fig, ax2, sc2, lambda i: f"Iter: {i+1}\nError: {errores[i]:.2e}")
        
        ax2.set_title('Error Absoluto')
        
        plt.tight_layout()
        self._mostrar_canvas(fig, self.graficas_frame)

    def _mostrar_canvas(self, fig, parent_frame):
        """Muestra la figura en el frame dado limpiando lo anterior"""
        for widget in parent_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        
        # Añadir barra de herramientas (Zoom, Pan, Save)
        toolbar = NavigationToolbar2Tk(canvas, parent_frame)
        toolbar.update()
        
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _crear_texto_con_scroll(self, parent, text_content):
        """Crea un widget de texto con scrollbar vertical"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        txt = tk.Text(frame, height=4, wrap=tk.WORD, font=FONT_MAIN,
                      yscrollcommand=scrollbar.set, relief="flat", bg=COLOR_BG)
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=txt.yview)

        txt.insert(tk.END, text_content)
        txt.config(state=tk.DISABLED)

    def comparar_biseccion_falsa(self, f, a, b, tol, max_iter):
        comparacion = comparar_biseccion_falsa_posicion(f, a, b, tol)
        
        # Limpiar frame
        for widget in self.comparacion_frame.winfo_children():
            widget.destroy()
            
        # Título
        ttk.Label(self.comparacion_frame, text="Comparativa de Rendimiento", style="Header.TLabel").pack(pady=10)
        
        # Análisis de texto (MOVER ARRIBA)
        analisis_frame = ttk.LabelFrame(self.comparacion_frame, text="Análisis de Convergencia", padding=15)
        analisis_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        
        comp = comparacion['comparacion']
        iter_bis = comp['iteraciones_biseccion']
        iter_falsa = comp['iteraciones_falsa']
        iter_diff = abs(iter_bis - iter_falsa)
        
        if iter_falsa < iter_bis:
            resumen = "El método de Falsa Posición convergió con menos iteraciones."
            analisis = (
                "Análisis: El método de Falsa Posición aprovecha la magnitud de f(x) en los extremos para interpolar la raíz. "
                "En funciones suaves, esto permite acercarse más rápido a la solución que dividir el intervalo a la mitad (Bisección)."
            )
        elif iter_bis < iter_falsa:
            resumen = "El método de Bisección convergió con menos iteraciones."
            analisis = (
                "Análisis: Bisección fue más eficiente en este caso. Esto ocurre cuando la función presenta una curvatura tal que "
                "la interpolación lineal (Falsa Posición) avanza muy lentamente por uno de los extremos, mientras que Bisección reduce el intervalo consistentemente."
            )
        else:
            resumen = "Ambos métodos convergieron en el mismo número de iteraciones."
            analisis = "Análisis: El rendimiento en iteraciones fue idéntico para la tolerancia y función dadas."
        
        texto_analisis = f"{resumen}\n\nDiferencia en iteraciones: {iter_diff}\n\n{analisis}"
        
        self._crear_texto_con_scroll(analisis_frame, texto_analisis)

        # Tabla
        columns = ('Método', 'Iteraciones', 'Raíz Encontrada', 'Tiempo (s)', 'Error final')

        # Nota: _crear_tabla usa self.resultados_frame por defecto, así que mejor creamos uno local aquí
        
        frame_tabla = ttk.Frame(self.comparacion_frame, style="Card.TFrame")
        frame_tabla.pack(fill=tk.X, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=4)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=tk.CENTER)
        tree.pack(fill=tk.X)
        
        bisec = comparacion['biseccion']
        falsa = comparacion['falsa_posicion']
        
        tree.insert('', tk.END, values=('Bisección', bisec['iteraciones_totales'], f"{bisec['raiz']:.8f}", f"{bisec['tiempo_ejecucion']:.6f}", f"{bisec['error_final']:.2e}"))
        tree.insert('', tk.END, values=('Falsa Posición', falsa['iteraciones_totales'], f"{falsa['raiz']:.8f}", f"{falsa['tiempo_ejecucion']:.6f}", f"{falsa['error_final']:.2e}"))

        # Gráfica comparativa
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        self._configurar_grafica(fig, [ax])
        
        errores_bisec = [it['error_abs'] for it in bisec['iteraciones']]
        errores_falsa = [it['error_abs'] for it in falsa['iteraciones']]
        
        self._graficar_error_log(fig, ax, errores_bisec, color='blue', label='Bisección')
        self._graficar_error_log(fig, ax, errores_falsa, color='red', label='Falsa Posición', marker='s')
        
        ax.legend()
        ax.set_title('Velocidad de Convergencia')
        
        canvas = FigureCanvasTkAgg(fig, master=self.comparacion_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    def comparar_newton_secante_ui(self, f, f_derivada, x0_newton, x0_secante, x1_secante, tol):
        comparacion = comparar_newton_secante(f, f_derivada, x0_newton, x0_secante, x1_secante, tol)
        
        for widget in self.comparacion_frame.winfo_children():
            widget.destroy()
            
        ttk.Label(self.comparacion_frame, text="Newton-Raphson vs Secante", style="Header.TLabel").pack(pady=10)
        
        # Análisis de texto (MOVER ARRIBA)
        analisis_frame = ttk.LabelFrame(self.comparacion_frame, text="Análisis de Costo-Beneficio", padding=15)
        analisis_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        
        comp = comparacion['comparacion']
        metodo_rapido = "Newton-Raphson" if comp['metodo_mas_rapido'] == 'newton' else "Secante"
        metodo_menos_eval = "Newton-Raphson" if comp['metodo_menos_evaluaciones'] == 'newton' else "Secante"
        
        texto_analisis = (
            f"Método más rápido en tiempo: {metodo_rapido}\n"
            f"Método con menos evaluaciones de función: {metodo_menos_eval}\n\n"
            "Análisis: Newton-Raphson tiene convergencia cuadrática (más rápida por iteración) pero requiere calcular la derivada analítica, "
            "lo cual puede ser costoso o difícil. El método de la Secante tiene convergencia superlineal (ligeramente más lenta) "
            "pero no requiere derivada explícita. \n\n"
            "Conclusión: Si la derivada es difícil de obtener, la Secante es preferible ya que ofrece un excelente equilibrio entre velocidad y simplicidad."
        )
        
        self._crear_texto_con_scroll(analisis_frame, texto_analisis)

        columns = ('Método', 'Iteraciones', 'Evaluaciones', 'Tiempo (s)', 'Error final')
        frame_tabla = ttk.Frame(self.comparacion_frame, style="Card.TFrame")
        frame_tabla.pack(fill=tk.X, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=4)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)
        tree.pack(fill=tk.X)
        
        newton = comparacion['newton']
        sec = comparacion['secante']
        
        tree.insert('', tk.END, values=('Newton', comp['iteraciones_newton'], comp['evaluaciones_newton'], f"{comp['tiempo_newton']:.6f}", f"{newton['error_final']:.2e}"))
        tree.insert('', tk.END, values=('Secante', comp['iteraciones_secante'], comp['evaluaciones_secante'], f"{comp['tiempo_secante']:.6f}", f"{sec['error_final']:.2e}"))
        
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        self._configurar_grafica(fig, [ax])
        
        errores_newton = [it['error_abs'] for it in newton['iteraciones']]
        errores_secante = [it['error_abs'] for it in sec['iteraciones']]
        
        self._graficar_error_log(fig, ax, errores_newton, color='blue', label='Newton')
        self._graficar_error_log(fig, ax, errores_secante, color='red', label='Secante', marker='s')
        
        ax.legend()
        ax.set_title('Convergencia del Error')
        
        canvas = FigureCanvasTkAgg(fig, master=self.comparacion_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    def comparar_punto_fijo_ui(self, g, g_derivada, tol):
        """Realiza el análisis de sensibilidad para Punto Fijo"""
        valores_iniciales = [0.5, 1.0, 1.5, 2.0]
        resultados = punto_fijo_multiple_inicial(g, valores_iniciales, g_derivada, tol)
        
        # Limpiar frame
        for widget in self.comparacion_frame.winfo_children():
            widget.destroy()
            
        ttk.Label(self.comparacion_frame, text="Análisis de Sensibilidad (Punto Fijo)", style="Header.TLabel").pack(pady=10)
        
        # Análisis de texto (MOVER ARRIBA)
        analisis_frame = ttk.LabelFrame(self.comparacion_frame, text="Conclusión del Análisis", padding=15)
        analisis_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        
        texto = (
            "Análisis: El valor inicial afecta directamente el número de iteraciones necesarias para alcanzar la tolerancia. "
            "Valores iniciales más cercanos a la raíz verdadera convergen más rápido. "
            "Si el valor inicial está muy lejos o en una región donde |g'(x)| >= 1, el método podría diverger o converger muy lentamente."
        )
        self._crear_texto_con_scroll(analisis_frame, texto)

        # Tabla
        columns = ('x0', 'Iteraciones', 'Raíz Encontrada', 'Convergió')
        frame_tabla = ttk.Frame(self.comparacion_frame, style="Card.TFrame")
        frame_tabla.pack(fill=tk.X, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=5)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)
        tree.pack(fill=tk.X)
        
        # Gráfica
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        self._configurar_grafica(fig, [ax])
        
        colores = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f']
        
        for i, x0 in enumerate(valores_iniciales):
            key = f"x0_{x0}"
            res = resultados[key]
            
            raiz_str = f"{res['raiz']:.8f}" if res['raiz'] else "N/A"
            conv_str = "Sí" if res['convergio'] else "No"
            
            tree.insert('', tk.END, values=(x0, res['iteraciones_totales'], raiz_str, conv_str))
            
            if res['iteraciones']:
                errores = [it['error_abs'] for it in res['iteraciones']]
                self._graficar_error_log(fig, ax, errores, color=colores[i % len(colores)], label=f'x0={x0}')

        ax.legend()
        ax.set_title('Convergencia según Valor Inicial')
        ax.set_xlabel('Iteración')
        ax.set_ylabel('Error Absoluto (log)')
        
        canvas = FigureCanvasTkAgg(fig, master=self.comparacion_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
    def comparar_newton_iniciales_ui(self, f, f_derivada, tol):
        """Realiza el análisis de sensibilidad para Newton-Raphson"""
        valores_iniciales = [1.0, 2.0, 3.0, 5.0]
        resultados = newton_multiple_inicial(f, f_derivada, valores_iniciales, tol)
        
        # Limpiar frame
        for widget in self.comparacion_frame.winfo_children():
            widget.destroy()
            
        ttk.Label(self.comparacion_frame, text="Análisis de Sensibilidad (Newton-Raphson)", style="Header.TLabel").pack(pady=10)
        
        # Análisis de texto (MOVER ARRIBA)
        analisis_frame = ttk.LabelFrame(self.comparacion_frame, text="Conclusión del Análisis", padding=15)
        analisis_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        
        mejor_x0 = None
        min_iter = float('inf')
        
        # Pre-calcular mejor x0 para el texto
        for x0 in valores_iniciales:
            res = resultados[f"x0_{x0}"]
            if res['convergio'] and res['iteraciones_totales'] < min_iter:
                min_iter = res['iteraciones_totales']
                mejor_x0 = x0

        texto = (
            f"El valor inicial que convergió más rápido fue x0 = {mejor_x0} con {min_iter} iteraciones.\n\n"
            "Análisis: El método de Newton-Raphson es muy sensible al valor inicial. "
            "Aunque su convergencia es cuadrática (muy rápida) cerca de la raíz, si el punto inicial está lejos "
            "o cerca de un punto donde la derivada es cero (punto crítico), puede diverger o converger lentamente. "
            "En este caso, se observa cómo la elección de x0 afecta drásticamente el número de iteraciones."
        )
        self._crear_texto_con_scroll(analisis_frame, texto)

        # Tabla
        columns = ('x0', 'Iteraciones', 'Raíz Encontrada', 'Convergió')
        frame_tabla = ttk.Frame(self.comparacion_frame, style="Card.TFrame")
        frame_tabla.pack(fill=tk.X, pady=10)
        
        tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=5)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)
        tree.pack(fill=tk.X)
        
        # Gráfica
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        self._configurar_grafica(fig, [ax])
        
        colores = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f']
        
        for i, x0 in enumerate(valores_iniciales):
            key = f"x0_{x0}"
            res = resultados[key]
            
            raiz_str = f"{res['raiz']:.8f}" if res['raiz'] else "N/A"
            conv_str = "Sí" if res['convergio'] else "No"
            
            tree.insert('', tk.END, values=(x0, res['iteraciones_totales'], raiz_str, conv_str))
            
            if res['iteraciones']:
                errores = [it['error_abs'] for it in res['iteraciones']]
                self._graficar_error_log(fig, ax, errores, color=colores[i % len(colores)], label=f'x0={x0}')

        ax.legend()
        ax.set_title('Convergencia según Valor Inicial')
        ax.set_xlabel('Iteración')
        ax.set_ylabel('Error Absoluto (log)')
        
        canvas = FigureCanvasTkAgg(fig, master=self.comparacion_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
    
    def limpiar(self):
        self.limpiar_pestanas()
        self.tolerancia_entry.delete(0, tk.END)
        self.tolerancia_entry.insert(0, "1e-6")
        self.max_iter_entry.delete(0, tk.END)
        self.max_iter_entry.insert(0, "100")
    
    def limpiar_pestanas(self):
        for frame in [self.resultados_frame, self.graficas_frame, 
                     self.comparacion_frame, self.analisis_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

def main():
    root = tk.Tk()
    app = MetodosNumericosGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()