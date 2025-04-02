# hotels.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk  # Importa ThemedTk para temas modernos
from database import connect_to_database  # Importa la conexión a la base de datos

# Función para cargar hoteles disponibles con filtros
def load_available_hotels(tree, ciudad=None):
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        query = "SELECT id_hotel, nombre, ciudad, fecha_disponible, precio_noche FROM hoteles WHERE 1=1"
        params = []

        if ciudad:
            query += " AND ciudad = %s"
            params.append(ciudad)

        cursor.execute(query, params)
        hotels = cursor.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        for hotel in hotels:
            tree.insert("", "end", values=hotel)

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al consultar hoteles: {e}")

    finally:
        cursor.close()
        connection.close()

# Función para comprar un hotel
def buy_hotel(tree, entry_noches):
    selected_item = tree.selection()  # Obtener el elemento seleccionado
    if not selected_item:
        tk.messagebox.showerror("Error", "Por favor, selecciona un hotel.")
        return

    try:
        noches = int(entry_noches.get().strip())
        if noches <= 0:
            tk.messagebox.showerror("Error", "El número de noches debe ser mayor a 0.")
            return
    except ValueError:
        tk.messagebox.showerror("Error", "Por favor, ingresa un número válido de noches.")
        return

    hotel_details = tree.item(selected_item)["values"]
    id_hotel, nombre, ciudad, fecha_disponible, precio_noche = hotel_details
    total_precio = precio_noche * noches

    confirm = tk.messagebox.askyesno("Confirmar Compra", f"¿Deseas confirmar la reserva?\n\n"
                                                        f"Hotel: {nombre}\n"
                                                        f"Ciudad: {ciudad}\n"
                                                        f"Noches: {noches}\n"
                                                        f"Precio Total: ${total_precio}")
    if confirm:
        reservation_id = save_hotel_reservation(id_hotel, noches)
        if reservation_id:
            tk.messagebox.showinfo("Éxito", f"¡Reserva realizada con éxito!\n"
                                           f"ID de tu reserva: {reservation_id}")
        load_available_hotels(tree)  # Actualizar la tabla

# Función para guardar la reserva del hotel en la base de datos
def save_hotel_reservation(id_hotel, noches):
    connection = connect_to_database()
    if not connection:
        return None

    cursor = connection.cursor()

    try:
        query = "INSERT INTO reservas_hoteles (id_hotel, noches) VALUES (%s, %s)"
        cursor.execute(query, (id_hotel, noches))
        connection.commit()

        reservation_id = cursor.lastrowid
        return reservation_id

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al guardar la reserva: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

# Función para abrir la ventana de hoteles
def open_hotels_window(parent):
    parent.withdraw()  # Oculta la ventana del dashboard

    # Crear la ventana de hoteles
    hotels_window = ThemedTk(theme="arc")  # Usa el tema "arc"
    hotels_window.title("Hoteles Disponibles")
    hotels_window.geometry("800x600")
    hotels_window.resizable(False, False)

    # Etiqueta de título
    tk.Label(hotels_window, text="Buscar Hoteles", font=("Arial", 16, "bold")).pack(pady=10)

    # Filtro por ciudad
    tk.Label(hotels_window, text="Filtrar por Ciudad:", font=("Arial", 12)).pack(pady=5)
    entry_ciudad = tk.Entry(hotels_window, font=("Arial", 12))
    entry_ciudad.pack(pady=5)

    # Botón para aplicar filtro
    tk.Button(hotels_window, text="Buscar Hoteles", font=("Arial", 12),
              command=lambda: load_available_hotels(tree, entry_ciudad.get().strip())).pack(pady=10)

    # Tabla para mostrar los hoteles disponibles
    columns = ("ID Hotel", "Nombre", "Ciudad", "Fecha Disponible", "Precio por Noche")
    tree = ttk.Treeview(hotels_window, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(pady=10)

    # Cargar hoteles al abrir la ventana
    load_available_hotels(tree)

    # Campo para ingresar el número de noches
    tk.Label(hotels_window, text="Noches a Quedarse:", font=("Arial", 12)).pack(pady=5)
    entry_noches = tk.Entry(hotels_window, font=("Arial", 12))
    entry_noches.pack(pady=5)

    # Botón para comprar un hotel
    tk.Button(hotels_window, text="Comprar Hotel", font=("Arial", 12),
              command=lambda: buy_hotel(tree, entry_noches)).pack(pady=10)

    # Botón para regresar al dashboard
    tk.Button(hotels_window, text="Regresar al Dashboard", font=("Arial", 12),
              command=lambda: close_hotels_window(hotels_window, parent)).pack(pady=10)

# Función para cerrar la ventana de hoteles
def close_hotels_window(hotels_window, parent):
    hotels_window.destroy()  # Cierra la ventana de hoteles
    parent.deiconify()  # Muestra nuevamente el dashboard
