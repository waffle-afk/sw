# flights.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk  # Importa ThemedTk para temas modernos
from database import connect_to_database  # Importa la conexión a la base de datos

# Función para cargar vuelos disponibles con filtros
def load_available_flights(tree, origen=None, destino=None, precio_min=None, precio_max=None):
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        query = "SELECT id_vuelo, origen, destino, fecha, hora_salida, precio FROM vuelos WHERE 1=1"
        params = []

        if origen:
            query += " AND origen = %s"
            params.append(origen)
        if destino:
            query += " AND destino = %s"
            params.append(destino)
        if precio_min:
            query += " AND precio >= %s"
            params.append(precio_min)
        if precio_max:
            query += " AND precio <= %s"
            params.append(precio_max)

        cursor.execute(query, params)
        flights = cursor.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        for flight in flights:
            tree.insert("", "end", values=flight)

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al consultar vuelos: {e}")

    finally:
        cursor.close()
        connection.close()

# Función para comprar un vuelo
def buy_flight(tree):
    selected_item = tree.selection()  # Obtener el elemento seleccionado
    if not selected_item:
        tk.messagebox.showerror("Error", "Por favor, selecciona un vuelo.")
        return

    flight_details = tree.item(selected_item)["values"]
    id_vuelo, origen, destino, fecha, hora_salida, precio = flight_details

    confirm = tk.messagebox.askyesno("Confirmar Compra", f"¿Deseas confirmar la compra?\n\n"
                                                        f"Origen: {origen}\n"
                                                        f"Destino: {destino}\n"
                                                        f"Fecha: {fecha}\n"
                                                        f"Hora Salida: {hora_salida}\n"
                                                        f"Precio: ${precio}")
    if confirm:
        reservation_id = save_flight_reservation(id_vuelo)
        if reservation_id:
            tk.messagebox.showinfo("Éxito", f"¡Reserva realizada con éxito!\n"
                                           f"ID de tu reserva: {reservation_id}")
        load_available_flights(tree)  # Actualizar la tabla

# Función para guardar la reserva del vuelo en la base de datos
def save_flight_reservation(id_vuelo):
    connection = connect_to_database()
    if not connection:
        return None

    cursor = connection.cursor()

    try:
        query = "INSERT INTO reservas (id_vuelo) VALUES (%s)"
        cursor.execute(query, (id_vuelo,))
        connection.commit()

        reservation_id = cursor.lastrowid
        return reservation_id

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al guardar la reserva: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

# Función para abrir la ventana de vuelos
def open_flights_window(parent):
    parent.withdraw()  # Oculta la ventana del dashboard

    # Crear la ventana de vuelos
    flights_window = ThemedTk(theme="arc")  # Usa el tema "arc"
    flights_window.title("Comprar Vuelos")
    flights_window.geometry("800x600")
    flights_window.resizable(False, False)

    # Etiqueta de título
    tk.Label(flights_window, text="Buscar Vuelos", font=("Arial", 16, "bold")).pack(pady=10)

    # Filtros
    tk.Label(flights_window, text="Origen:", font=("Arial", 12)).pack(pady=5)
    entry_origen = tk.Entry(flights_window, font=("Arial", 12))
    entry_origen.pack(pady=5)

    tk.Label(flights_window, text="Destino:", font=("Arial", 12)).pack(pady=5)
    entry_destino = tk.Entry(flights_window, font=("Arial", 12))
    entry_destino.pack(pady=5)

    # Botón para aplicar filtros
    tk.Button(flights_window, text="Aplicar Filtros", font=("Arial", 12),
              command=lambda: load_available_flights(tree,
                                                     entry_origen.get().strip(),
                                                     entry_destino.get().strip())).pack(pady=10)

    # Tabla para mostrar los vuelos disponibles
    columns = ("ID", "Origen", "Destino", "Fecha", "Hora Salida", "Precio")
    tree = ttk.Treeview(flights_window, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(pady=10)

    # Cargar vuelos al abrir la ventana
    load_available_flights(tree)

    # Botón para comprar un vuelo
    tk.Button(flights_window, text="Comprar Vuelo", font=("Arial", 12),
              command=lambda: buy_flight(tree)).pack(pady=10)

    # Botón para regresar al dashboard
    tk.Button(flights_window, text="Regresar al Dashboard", font=("Arial", 12),
              command=lambda: close_flights_window(flights_window, parent)).pack(pady=10)

# Función para cerrar la ventana de vuelos
def close_flights_window(flights_window, parent):
    flights_window.destroy()  # Cierra la ventana de vuelos
    parent.deiconify()  # Muestra nuevamente el dashboard
