-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS hotel_db;

-- Usar la base de datos
USE hotel_db;

-- Crear la tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    tipo ENUM('cliente', 'admin') DEFAULT 'cliente'
);

-- Crear la tabla de habitaciones
CREATE TABLE IF NOT EXISTS habitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) UNIQUE NOT NULL,
    tipo ENUM('simple', 'doble', 'suite') NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    estado ENUM('disponible', 'ocupada') DEFAULT 'disponible'
);

-- Crear la tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    habitacion_id INT NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
);

-- Insertar usuarios de ejemplo
INSERT INTO usuarios (nombre, username, password, tipo) VALUES ('Administrador', 'admin', 'admin123', 'admin');
INSERT INTO usuarios (nombre, username, password, tipo) VALUES ('Cliente 1', 'cliente1', 'cliente123', 'cliente');
