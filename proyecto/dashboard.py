# dashboard.py

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from flights import open_flights_window  # Importa la función para abrir la ventana de vuelos
from reservations import open_reservations_window  # Importa la función para abrir la ventana de reservas
from hotels import open_hotels_window  # Importa la función para abrir la ventana de hoteles

# Función para abrir el dashboard
def open_dashboard(username):
    dashboard_window = ThemedTk(theme="equilux")  # Tema moderno oscuro
    dashboard_window.title("Dashboard - Agencia de Viajes")
    dashboard_window.geometry("700x500")
    dashboard_window.resizable(False, False)
    
    # Configuración de estilos
    style = ttk.Style(dashboard_window)
    style.configure("TLabel", font=("Helvetica", 11))
    style.configure("TButton", font=("Helvetica", 11), padding=10)
    style.configure("Title.TLabel", font=("Helvetica", 22, "bold"))
    style.configure("Accent.TButton", font=("Helvetica", 11, "bold"))
    
    # Marco principal con padding
    main_frame = ttk.Frame(dashboard_window, padding=(30, 20))
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Encabezado con mensaje de bienvenida
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 30))
    
    welcome_label = ttk.Label(
        header_frame, 
        text=f"Bienvenido, {username}", 
        style="Title.TLabel"
    )
    welcome_label.pack(side=tk.LEFT, anchor=tk.W)
    
    # Separador
    separator = ttk.Separator(main_frame, orient="horizontal")
    separator.pack(fill=tk.X, pady=(0, 30))
    
    # Marco para los botones principales
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Contenedor para organizar los botones en una cuadrícula
    grid_frame = ttk.Frame(button_frame)
    grid_frame.pack(fill=tk.BOTH, expand=True, padx=20)
    
    # Configurar el grid con 2 columnas
    grid_frame.columnconfigure(0, weight=1)
    grid_frame.columnconfigure(1, weight=1)
    
    # Crear iconos de texto (ya que no podemos usar imágenes reales)
    icon_styles = {
        "vuelos": "✈️",
        "reservas": "🔖",
        "hoteles": "🏨",
        "salir": "🚪"
    }
    
    # Botones principales con íconos de texto
    vuelos_button = ttk.Button(
        grid_frame, 
        text=f"{icon_styles['vuelos']}  Comprar Vuelos",
        command=lambda: open_flights_window(dashboard_window),
        style="Accent.TButton"
    )
    vuelos_button.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")
    
    reservas_button = ttk.Button(
        grid_frame, 
        text=f"{icon_styles['reservas']}  Gestionar Reservas",
        command=lambda: open_reservations_window(dashboard_window),
        style="Accent.TButton"
    )
    reservas_button.grid(row=0, column=1, padx=10, pady=15, sticky="nsew")
    
    hoteles_button = ttk.Button(
        grid_frame, 
        text=f"{icon_styles['hoteles']}  Ver Hoteles",
        command=lambda: open_hotels_window(dashboard_window),
        style="Accent.TButton"
    )
    hoteles_button.grid(row=1, column=0, padx=10, pady=15, sticky="nsew")
    
    # Marco para el pie de página
    footer_frame = ttk.Frame(main_frame)
    footer_frame.pack(fill=tk.X, pady=(30, 0))
    
    # Segundo separador
    separator2 = ttk.Separator(footer_frame, orient="horizontal")
    separator2.pack(fill=tk.X, pady=(0, 20))
    
    # Botón de cerrar sesión en la parte inferior
    logout_button = ttk.Button(
        footer_frame, 
        text=f"{icon_styles['salir']}  Cerrar Sesión",
        command=dashboard_window.destroy
    )
    logout_button.pack(side=tk.RIGHT, pady=10)
    
    # Información de la versión
    version_label = ttk.Label(footer_frame, text="v1.0", foreground="gray")
    version_label.pack(side=tk.LEFT, pady=10)
    
    # Centrar la ventana
    dashboard_window.update_idletasks()
    width = dashboard_window.winfo_width()
    height = dashboard_window.winfo_height()
    x = (dashboard_window.winfo_screenwidth() // 2) - (width // 2)
    y = (dashboard_window.winfo_screenheight() // 2) - (height // 2)
    dashboard_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    dashboard_window.mainloop()

