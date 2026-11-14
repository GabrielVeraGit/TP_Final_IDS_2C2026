CREATE DATABASE IF NOT EXISTS CINE_PARADISO;
USE CINE_PARADISO;

CREATE TABLE IF NOT EXISTS SEDES (
    id_sede INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS USUARIOS (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(500) NOT NULL,
    rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente'
);

CREATE TABLE IF NOT EXISTS SALAS (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    id_sede INT NOT NULL,
    numero VARCHAR(50) NOT NULL,
    capacidad INT NOT NULL,
    FOREIGN KEY (id_sede) REFERENCES SEDES(id_sede) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS PELICULAS (
    id_pelicula INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    anio INT NOT NULL,
    clasificacion VARCHAR(10),
    duracion VARCHAR(50),
    genero VARCHAR(200),
    director VARCHAR(200),
    actores VARCHAR(200),
    sinopsis TEXT,
    lenguaje TEXT,
    poster VARCHAR(500),
    omdb_id VARCHAR(500),
    disponible_desde DATETIME NULL,     
    disponible_hasta DATETIME NULL,
    UNIQUE (omdb_id)
);

CREATE TABLE IF NOT EXISTS FUNCIONES (
    id_funcion INT AUTO_INCREMENT PRIMARY KEY,
    id_pelicula INT NOT NULL,
    id_sala INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    precio_entrada DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pelicula) REFERENCES PELICULAS(id_pelicula) ON DELETE CASCADE,
    FOREIGN KEY (id_sala) REFERENCES SALAS(id_sala) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS RESERVAS (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_funcion INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_de_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    qr VARCHAR(255) NOT NULL UNIQUE,
    estado_compra ENUM('reservada', 'cancelada', 'usada') NOT NULL DEFAULT 'reservada',
    cant_entradas INT NOT NULL,
    monto_a_pagar DECIMAL(10,2) NOT NULL,
    fecha_cancelacion DATETIME NULL,
    fecha_validacion DATETIME NULL,
    FOREIGN KEY (id_funcion) REFERENCES FUNCIONES(id_funcion) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS EMAILS_ADMIN(
    id_email INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Datos de prueba

INSERT INTO EMAILS_ADMIN (email) VALUES ('admin.cineparadiso@gmail.com');

INSERT INTO SEDES (nombre, direccion) VALUES
('Paradiso Centro', 'Av. Corrientes 1234, CABA'),
('Paradiso Belgrano', 'Av. Cabildo 2050, CABA'),
('Paradiso Palermo', 'Av. Santa Fe 3300, CABA');

INSERT INTO SALAS (id_sede, numero, capacidad) VALUES
(1, 'Sala 1', 120),
(1, 'Sala 2', 80),
(2, 'Sala 1', 100),
(2, 'Sala 2', 60),
(3, 'Sala 1', 150),
(3, 'Sala 2', 40);

INSERT INTO PELICULAS (titulo, anio, clasificacion, duracion, genero, director, actores, sinopsis, lenguaje, poster, omdb_id, disponible_desde, disponible_hasta) VALUES
('2012', 2009, 'PG-13', '158 min', 'Action, Adventure, Sci-Fi', 'Roland Emmerich', 'John Cusack, Thandiwe Newton, Chiwetel Ejiofor',
 'A frustrated writer struggles to keep his family alive when a series of global catastrophes threatens to annihilate mankind.',
 'English, French, Tibetan, Mandarin, Russian, Hindi, Portuguese, Latin, Italian, Spanish',
 'https://m.media-amazon.com/images/M/MV5BMTY0MjEyODQzMF5BMl5BanBnXkFtZTcwMTczMjQ4Mg@@._V1_QL75_UX380_CR0,1,380,562_.jpg',
 'tt1190080', '2026-11-01 00:00:00', '2026-12-31 23:59:59'),
('The Matrix', 1999, 'R', '136 min', 'Action, Sci-Fi', 'Lana Wachowski, Lilly Wachowski', 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
 'When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.',
 'English', 'https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_SX300.jpg',
 'tt0133093', '2026-11-01 00:00:00', '2026-12-31 23:59:59'),
('Back to the Future', 1985, 'PG', '116 min', 'Adventure, Comedy, Sci-Fi', 'Robert Zemeckis', 'Michael J. Fox, Christopher Lloyd, Lea Thompson',
 'Marty McFly, a 17-year-old high school student, is accidentally sent 30 years into the past in a time-traveling DeLorean invented by his close friend, the maverick scientist Doc Brown.',
 'English', 'https://m.media-amazon.com/images/M/MV5BZmM3ZjE0NzctNjBiOC00MDZmLTgzMTUtNGVlOWFlOTNiZDJiXkEyXkFqcGc@._V1_SX300.jpg',
 'tt0088763', '2026-11-01 00:00:00', '2026-12-31 23:59:59');

INSERT INTO FUNCIONES (id_pelicula, id_sala, fecha_hora, precio_entrada) VALUES
(1, 1, '2026-11-25 18:00:00', 6500.00),
(1, 3, '2026-11-25 21:30:00', 6500.00),
(2, 2, '2026-11-26 20:00:00', 6000.00),
(2, 5, '2026-11-27 19:00:00', 6000.00),
(3, 4, '2026-11-28 17:00:00', 5500.00),
(3, 6, '2026-12-05 22:00:00', 5500.00);


