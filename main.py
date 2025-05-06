from colorama import Cursor
from config import conectar_db
import hashlib
import sys

# Función para registrar un nuevo usuario
def registrar_usuario():
    nombre = input("\nIngrese su nombre completo: ")
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    # Encriptar la contraseña
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Conectar a la base de datos
    conn = conectar_db()
    cursor = conn.cursor()

    # Verificar si el nombre de usuario ya existe
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    if cursor.fetchone():
        print("El nombre de usuario ya está registrado. Por favor, elige otro.")
        conn.close()
        return

    # Insertar el nuevo usuario en la base de datos
    cursor.execute("INSERT INTO usuarios (nombre, username, password, tipo) VALUES (%s, %s, %s, %s)",
                   (nombre, username, password_hash, 'cliente'))
    conn.commit()
    print("\n¡Registro exitoso! Puedes iniciar sesión desde el menú principal.")
    conn.close()

# Función para realizar el login
def login():
    username = input("\nIngrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    # Encriptar la contraseña ingresada
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Conectar a la base de datos
    conn = conectar_db()
    cursor = conn.cursor()

    # Verificar si el usuario existe en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password_hash))
    user = cursor.fetchone()

    if user:
        print(f"\n   Bienvenido, {user[1]}!")
        return user
    else:
        print("\nUsuario o contraseña incorrectos.")
        return None

# Función para mostrar el menú principal
def mostrar_menu():
    print("\n--- Menú ---")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir del programa")


# Función para ver habitaciones disponibles
def ver_habitaciones():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM habitaciones WHERE estado = 'disponible'")
    habitaciones = cursor.fetchall()

    if habitaciones:
        print("\nHabitaciones disponibles:")
        for habitacion in habitaciones:
            print(f"ID: {habitacion[0]}, Número: {habitacion[1]}, Tipo: {habitacion[2]}, Precio: {habitacion[3]}")
    else:
        print("\nNo hay habitaciones disponibles.")
    
    conn.close()

# Función para realizar una reserva
def realizar_reserva(usuario_id):
    conn = conectar_db()
    cursor = conn.cursor()

    ver_habitaciones()

    print("\nEscriba 'cancelar' en cualquier momento para volver al menú sin hacer la reserva.")

    # Ingresar ID habitación
    habitacion_input = input("\nIngrese el ID de la habitación que desea reservar: ").strip()
    if habitacion_input.lower() == 'cancelar':
        print("\nReserva cancelada. Volviendo al menú.")
        conn.close()
        return
    if not habitacion_input.isdigit():
        print("❌ Entrada inválida. Debe ser un número.")
        conn.close()
        return
    habitacion_id = int(habitacion_input)

    # Ingresar fecha de entrada
    fecha_entrada = input("Ingrese la fecha de entrada (YYYY-MM-DD): ").strip()
    if fecha_entrada.lower() == 'cancelar':
        print("\nReserva cancelada. Volviendo al menú.")
        conn.close()
        return

    # Ingresar fecha de salida
    fecha_salida = input("Ingrese la fecha de salida (YYYY-MM-DD): ").strip()
    if fecha_salida.lower() == 'cancelar':
        print("\nReserva cancelada. Volviendo al menú.")
        conn.close()
        return

    try:
        # Insertar la reserva
        cursor.execute("""
            INSERT INTO reservas (usuario_id, habitacion_id, fecha_entrada, fecha_salida)
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, habitacion_id, fecha_entrada, fecha_salida))
        conn.commit()

        # Cambiar estado a 'reservada'
        cursor.execute("UPDATE habitaciones SET estado = 'reservada' WHERE id = %s", (habitacion_id,))
        conn.commit()

        print("✅ Reserva realizada con éxito. La habitación fue marcada como 'reservada'.")
    except Exception as e:
        print(f"❌ Error al realizar la reserva: {e}")
    finally:
        conn.close()

# Función para ver las reservas del usuario
def ver_reservas(usuario_id):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservas WHERE usuario_id = %s", (usuario_id,))
    reservas = cursor.fetchall()

    if reservas:
        print("\nTus reservas:")
        for reserva in reservas:
            cursor.execute("SELECT numero, tipo FROM habitaciones WHERE id = %s", (reserva[2],))
            habitacion = cursor.fetchone()
            print(f"\nReserva ID: {reserva[0]}, Habitación: {habitacion[1]} {habitacion[0]}, Fecha Entrada: {reserva[3]}, Fecha Salida: {reserva[4]}")
    else:
        print("\nNo tienes reservas realizadas.")

    conn.close()