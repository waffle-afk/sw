# database.py

import mysql.connector
from mysql.connector import Error

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
        print(f"Error al conectar a la base de datos: {e}")
        return None
