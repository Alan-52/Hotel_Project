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