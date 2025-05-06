import mysql.connector

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Usuario por defecto en XAMPP
    'password': '',  # Contraseña vacía por defecto en XAMPP
    'database': 'hotel_db'
}

# Función para conectar a la base de datos
def conectar_db():
    """Conectar a la base de datos MySQL"""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

