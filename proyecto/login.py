# login.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import mysql.connector
from mysql.connector import Error
from dashboard import open_dashboard  # Importa la función para abrir el dashboard

# Función para conectar a la base de datos
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="nuevo_usuario",
            password="contraseña",
            database="agencia_viajes"
        )
        return connection
    except Error as e:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        return None

# Función para validar el login
def validate_login(entry_correo, entry_password, root):
    correo = entry_correo.get().strip()
    password = entry_password.get().strip()

    # Validar que los campos no estén vacíos
    if not correo or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    # Conectar a la base de datos
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        # Consultar las credenciales del usuario
        query = "SELECT nombre FROM usuarios WHERE correo = %s AND password = %s"
        cursor.execute(query, (correo, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
            root.destroy()  # Cierra la ventana de login
            open_dashboard(user[0])  # Abre el dashboard con el nombre del usuario
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")

    except Error as e:
        messagebox.showerror("Error", f"Error al consultar la base de datos: {e}")

    finally:
        cursor.close()
        connection.close()

# Función para registrar un nuevo usuario
def register_user(registro_window, entry_nombre, entry_correo, entry_password):
    nombre = entry_nombre.get().strip()
    correo = entry_correo.get().strip()
    password = entry_password.get().strip()

    # Validar que los campos no estén vacíos
    if not nombre or not correo or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    # Conectar a la base de datos
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        # Verificar si el correo ya existe
        query_check = "SELECT * FROM usuarios WHERE correo = %s"
        cursor.execute(query_check, (correo,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "El correo ya está registrado.")
        else:
            # Insertar el nuevo usuario
            query_insert = "INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)"
            cursor.execute(query_insert, (nombre, correo, password))
            connection.commit()
            messagebox.showinfo("Éxito", "Registro exitoso. Ahora puedes iniciar sesión.")
            registro_window.destroy()  # Cerrar la ventana de registro

    except Error as e:
        messagebox.showerror("Error", f"Error al registrar usuario: {e}")

    finally:
        cursor.close()
        connection.close()

# Función para abrir el formulario de registro
def open_register_form():
    # Crear una nueva ventana para el registro
    registro_window = ThemedTk(theme="equilux")  # Tema moderno oscuro
    registro_window.title("Registro de Usuario")
    registro_window.geometry("400x400")
    registro_window.resizable(False, False)

    # Crear un marco principal con padding
    main_frame = ttk.Frame(registro_window, padding=(20, 10))
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Etiqueta de título
    title_label = ttk.Label(main_frame, text="Registro de Usuario", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=(10, 20))

    # Marco para el formulario
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(fill=tk.BOTH, expand=True)

    # Etiquetas y campos de entrada
    ttk.Label(form_frame, text="Nombre:", font=("Helvetica", 11)).pack(anchor=tk.W, pady=(10, 0))
    entry_nombre = ttk.Entry(form_frame, font=("Helvetica", 11), width=30)
    entry_nombre.pack(fill=tk.X, pady=(5, 10))
    entry_nombre.focus()  # Auto-focus en el primer campo

    ttk.Label(form_frame, text="Correo Electrónico:", font=("Helvetica", 11)).pack(anchor=tk.W, pady=(10, 0))
    entry_correo = ttk.Entry(form_frame, font=("Helvetica", 11), width=30)
    entry_correo.pack(fill=tk.X, pady=(5, 10))

    ttk.Label(form_frame, text="Contraseña:", font=("Helvetica", 11)).pack(anchor=tk.W, pady=(10, 0))
    entry_password = ttk.Entry(form_frame, font=("Helvetica", 11), width=30, show="*")
    entry_password.pack(fill=tk.X, pady=(5, 10))

    # Botón para registrar con estilo
    style = ttk.Style(registro_window)
    style.configure("Accent.TButton", font=("Helvetica", 11, "bold"))
    
    register_button = ttk.Button(
        form_frame, 
        text="Registrar", 
        command=lambda: register_user(registro_window, entry_nombre, entry_correo, entry_password),
        style="Accent.TButton"
    )
    register_button.pack(pady=(20, 10), fill=tk.X)
    
    # Centrar la ventana
    registro_window.update_idletasks()
    width = registro_window.winfo_width()
    height = registro_window.winfo_height()
    x = (registro_window.winfo_screenwidth() // 2) - (width // 2)
    y = (registro_window.winfo_screenheight() // 2) - (height // 2)
    registro_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Función para abrir la ventana de login
def open_login_window():
    root = ThemedTk(theme="equilux")  # Tema moderno oscuro
    root.title("Sistema de Login")
    root.geometry("400x450")
    root.resizable(False, False)
    
    # Aplicar estilo personalizado
    style = ttk.Style(root)
    style.configure("TLabel", font=("Helvetica", 11))
    style.configure("TEntry", font=("Helvetica", 11))
    style.configure("TButton", font=("Helvetica", 11))
    style.configure("Accent.TButton", font=("Helvetica", 11, "bold"))
    style.configure("Link.TButton", font=("Helvetica", 10, "underline"))
    
    # Crear un marco principal con padding
    main_frame = ttk.Frame(root, padding=(20, 10))
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Etiqueta de título
    title_label = ttk.Label(main_frame, text="Iniciar Sesión", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(20, 30))
    
    # Marco para el formulario
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(fill=tk.BOTH, expand=True)

    # Campos de entrada
    ttk.Label(form_frame, text="Correo Electrónico:").pack(anchor=tk.W, pady=(10, 0))
    entry_correo = ttk.Entry(form_frame, width=30)
    entry_correo.pack(fill=tk.X, pady=(5, 10))
    entry_correo.focus()  # Auto-focus en el primer campo

    ttk.Label(form_frame, text="Contraseña:").pack(anchor=tk.W, pady=(10, 0))
    entry_password = ttk.Entry(form_frame, width=30, show="*")
    entry_password.pack(fill=tk.X, pady=(5, 10))

    # Botón de login con estilo
    login_button = ttk.Button(
        form_frame, 
        text="Iniciar Sesión",
        command=lambda: validate_login(entry_correo, entry_password, root),
        style="Accent.TButton"
    )
    login_button.pack(pady=(30, 10), fill=tk.X)

    # Separador
    separator = ttk.Separator(form_frame, orient="horizontal")
    separator.pack(fill=tk.X, pady=(20, 20))

    # Botón de registro con estilo de enlace
    register_button = ttk.Button(
        form_frame, 
        text="¿No tienes cuenta? Regístrate",
        command=open_register_form,
        style="Link.TButton"
    )
    register_button.pack(pady=5)
    
    # Centrar la ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # Ejecutar la aplicación
    root.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    open_login_window()
