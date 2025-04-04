import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import connect_to_database  # Importa la conexión a la base de datos

# Función para cargar reservas del usuario
def load_user_reservations(tree):
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        # Consultar reservas de vuelos
        query_flights = """
        SELECT r.id_reserva, 'Vuelo', v.origen, v.destino, CONCAT(r.num_pasajeros, ' pasajeros'), r.precio_total
        FROM reservas r
        JOIN vuelos v ON r.id_vuelo = v.id_vuelo
        """
        cursor.execute(query_flights)
        reservations = cursor.fetchall()

        # Consultar reservas de hoteles
        query_hotels = """
        SELECT rh.id_reserva_hotel, 'Hotel', h.nombre, h.ciudad, CONCAT(rh.noches, ' noches'), (h.precio_noche * rh.noches)
        FROM reservas_hoteles rh
        JOIN hoteles h ON rh.id_hotel = h.id_hotel
        """
        cursor.execute(query_hotels)
        reservations += cursor.fetchall()

        # Limpiar la tabla antes de mostrar nuevos resultados
        for row in tree.get_children():
            tree.delete(row)

        # Mostrar los resultados en la tabla
        for reservation in reservations:
            tree.insert("", "end", values=reservation)

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al consultar reservas: {e}")

    finally:
        cursor.close()
        connection.close()

# Función para cancelar una reserva
def cancel_reservation(tree):
    selected_item = tree.selection()
    if not selected_item:
        tk.messagebox.showerror("Error", "Por favor, selecciona una reserva.")
        return

    # Obtener los detalles de la reserva seleccionada
    reservation_details = tree.item(selected_item)["values"]
    reservation_id = reservation_details[0]
    reservation_type = reservation_details[1]  # "Vuelo" o "Hotel"

    # Confirmación del usuario
    confirm = tk.messagebox.askyesno("Confirmar Cancelación", "¿Deseas cancelar esta reserva?")
    if confirm:
        if reservation_type == "Vuelo":
            delete_flight_reservation(reservation_id)
        elif reservation_type == "Hotel":
            delete_hotel_reservation(reservation_id)
        tk.messagebox.showinfo("Éxito", "Reserva cancelada con éxito.")
        load_user_reservations(tree)  # Actualizar la tabla

# Función para eliminar una reserva de vuelo
def delete_flight_reservation(reservation_id):
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        # Obtener el número de pasajeros y el ID del vuelo
        cursor.execute("SELECT id_vuelo, num_pasajeros FROM reservas WHERE id_reserva = %s", (reservation_id,))
        result = cursor.fetchone()
        if not result:
            tk.messagebox.showerror("Error", "Reserva no encontrada.")
            return

        id_vuelo, num_pasajeros = result

        # Eliminar la reserva
        cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (reservation_id,))

        # Actualizar las plazas disponibles en la tabla vuelos
        cursor.execute("UPDATE vuelos SET plazas_disponibles = plazas_disponibles + %s WHERE id_vuelo = %s",
                       (num_pasajeros, id_vuelo))

        connection.commit()

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al cancelar la reserva de vuelo: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

# Función para eliminar una reserva de hotel
def delete_hotel_reservation(reservation_id):
    connection = connect_to_database()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        # Eliminar la reserva
        cursor.execute("DELETE FROM reservas_hoteles WHERE id_reserva_hotel = %s", (reservation_id,))
        connection.commit()

    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al cancelar la reserva de hotel: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

# Función para abrir la ventana de reservas
def open_reservations_window(parent):
    parent.withdraw()  # Oculta la ventana del dashboard

    # Crear la ventana de reservas
    reservations_window = tk.Toplevel(parent)
    reservations_window.title("Gestionar Reservas")
    reservations_window.geometry("800x600")
    reservations_window.resizable(False, False)

    # Etiqueta de título
    tk.Label(reservations_window, text="Mis Reservas", font=("Arial", 16, "bold")).pack(pady=10)

    # Tabla para mostrar las reservas
    columns = ("ID Reserva", "Tipo", "Origen/Destino/Hotel", "Ciudad", "Detalles", "Precio Total")
    tree = ttk.Treeview(reservations_window, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(pady=10)

    # Cargar reservas al abrir la ventana
    load_user_reservations(tree)

    # Botón para cancelar una reserva
    tk.Button(reservations_window, text="Cancelar Reserva", font=("Arial", 12),
              command=lambda: cancel_reservation(tree)).pack(pady=10)

    # Botón para regresar al dashboard
    tk.Button(reservations_window, text="Regresar al Dashboard", font=("Arial", 12),
              command=lambda: close_reservations_window(reservations_window, parent)).pack(pady=10)

# Función para cerrar la ventana de reservas
def close_reservations_window(reservations_window, parent):
    reservations_window.destroy()  # Cierra la ventana de reservas
    parent.deiconify()  # Muestra nuevamente el dashboard


