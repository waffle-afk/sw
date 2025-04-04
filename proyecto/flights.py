# flights.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from ttkthemes import ThemedTk  # Importa ThemedTk para temas modernos
from database import connect_to_database  # Importa la conexión a la base de datos

# Función para cargar vuelos disponibles con filtros
def load_available_flights(tree, origen=None, destino=None):
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        query = """
        SELECT id_vuelo, origen, destino, fecha, hora_salida, precio, plazas_disponibles 
        FROM vuelos 
        WHERE plazas_disponibles > 0
        """
        params = []

        if origen:
            query += " AND origen = %s"
            params.append(origen)
        if destino:
            query += " AND destino = %s"
            params.append(destino)

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
    id_vuelo, origen, destino, fecha, hora_salida, precio, plazas_disponibles = flight_details

    # Preguntar cuántos pasajeros desea reservar
    num_pasajeros = tk.simpledialog.askinteger(
        "Número de Pasajeros",
        "¿Cuántos pasajeros deseas reservar?",
        minvalue=1,
        maxvalue=plazas_disponibles
    )

    if not num_pasajeros:
        tk.messagebox.showerror("Error", "Debes ingresar un número válido de pasajeros.")
        return

    # Calcular el precio total
    precio_total = precio * num_pasajeros

    # Confirmar la compra
    confirm = tk.messagebox.askyesno("Confirmar Compra", f"¿Deseas confirmar la compra?\n\n"
                                                        f"Origen: {origen}\n"
                                                        f"Destino: {destino}\n"
                                                        f"Fecha: {fecha}\n"
                                                        f"Hora Salida: {hora_salida}\n"
                                                        f"Número de Pasajeros: {num_pasajeros}\n"
                                                        f"Precio Total: ${precio_total}")
    if confirm:
        reservation_id = save_flight_reservation(id_vuelo, num_pasajeros, precio_total)
        if reservation_id:
            tk.messagebox.showinfo("Éxito", f"¡Reserva realizada con éxito!\n"
                                           f"ID de tu reserva: {reservation_id}")
        load_available_flights(tree)  # Actualizar la tabla

# Función para guardar la reserva del vuelo en la base de datos
def save_flight_reservation(id_vuelo, num_pasajeros, precio_total):
    connection = connect_to_database()
    if not connection:
        return None

    cursor = connection.cursor()

    try:
        # Reducir las plazas disponibles
        cursor.execute("UPDATE vuelos SET plazas_disponibles = plazas_disponibles - %s WHERE id_vuelo = %s",
                       (num_pasajeros, id_vuelo))

        # Guardar la reserva en la tabla de reservas
        query = "INSERT INTO reservas (id_vuelo, num_pasajeros, precio_total) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_vuelo, num_pasajeros, precio_total))
        connection.commit()

        reservation_id = cursor.lastrowid
        return reservation_id

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al guardar la reserva: {e}")
        connection.rollback()
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

    # Cargar ciudades disponibles
    cities = load_cities()

    # Combobox para origen
    tk.Label(flights_window, text="Origen:", font=("Arial", 12)).pack(pady=5)
    combo_origen = ttk.Combobox(flights_window, font=("Arial", 12), values=cities, state="readonly")
    combo_origen.pack(pady=5)

    # Combobox para destino
    tk.Label(flights_window, text="Destino:", font=("Arial", 12)).pack(pady=5)
    combo_destino = ttk.Combobox(flights_window, font=("Arial", 12), values=cities, state="readonly")
    combo_destino.pack(pady=5)

    # Botón para aplicar filtros
    tk.Button(flights_window, text="Aplicar Filtros", font=("Arial", 12),
              command=lambda: load_available_flights(tree,
                                                     combo_origen.get(),
                                                     combo_destino.get())).pack(pady=10)

    # Tabla para mostrar los vuelos disponibles
    columns = ("ID", "Origen", "Destino", "Fecha", "Hora Salida", "Precio", "Plazas Disponibles")
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

# Función para cargar ciudades disponibles
def load_cities():
    connection = connect_to_database()
    if not connection:
        return []

    cursor = connection.cursor()

    try:
        # Consulta para obtener ciudades únicas de la tabla vuelos
        cursor.execute("SELECT DISTINCT origen FROM vuelos UNION SELECT DISTINCT destino FROM vuelos")
        cities = [city[0] for city in cursor.fetchall()]
        return cities

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al cargar ciudades: {e}")
        return []

    finally:
        cursor.close()
        connection.close()
