CREATE DATABASE Eduquest_db;
USE Eduquest_db;
DROP DATABASE Eduquest_db;

-- Tabla de roles
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

SELECT * FROM roles;
-- Insertar roles
INSERT INTO roles (nombre) VALUES ('alumno'), ('maestro'), ('admin');

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

SELECT * FROM usuarios;

-- Tabla de alumnos
CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    grado_id INT,
    especialidad_id INT,
    seccion_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (grado_id) REFERENCES grados(id),
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id),
    FOREIGN KEY (seccion_id) REFERENCES secciones(id)
);

-- Tabla de maestros
CREATE TABLE maestros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de materias
CREATE TABLE materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Tabla de grados
CREATE TABLE grados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Tabla de especialidades
CREATE TABLE especialidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
SELECT * FROM especialidades;

-- Tabla de secciones
CREATE TABLE secciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE TABLE asignacion_maestros (
    maestro_id INT,
    grado_id INT,
    materia_id INT,
    especialidad_id INT,
    seccion_id INT,
    PRIMARY KEY (maestro_id, grado_id, materia_id, especialidad_id),
    FOREIGN KEY (maestro_id) REFERENCES maestros(id),
    FOREIGN KEY (grado_id) REFERENCES grados(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id),
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id),
    FOREIGN KEY (seccion_id) REFERENCES secciones(id)
);

-- Tabla de examenes
CREATE TABLE examenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_examen VARCHAR(100) NOT NULL,
    grado_id INT,
    materia_id INT,
    especialidad_id INT,
    seccion_id INT,
    maestro_id INT,
    cantidad_preguntas INT NOT NULL,
    puntaje_total INT,
    fecha_publicacion DATE,
    fecha_entrega DATE,
    estado BOOL,
    aproved BOOL,
    comentario VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (grado_id) REFERENCES grados(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id),
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id),
    FOREIGN KEY (maestro_id) REFERENCES maestros(id),
    FOREIGN KEY (seccion_id) REFERENCES secciones(id)
);

-- Tabla de preguntas
CREATE TABLE preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    examen_id INT,
    pregunta TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (examen_id) REFERENCES examenes(id)
);

-- Tabla de respuestas
CREATE TABLE respuestas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta_id INT,
    respuesta TEXT NOT NULL,
    es_correcta BOOL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (pregunta_id) REFERENCES preguntas(id)
);

-- Tabla de preguntas_respondidas
CREATE TABLE preguntas_respondidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    examen_id INT,
    alumno_id INT,
    pregunta_id INT,
    respuesta_id INT,
    es_correcta BOOL,
    puntos_obtenidos DECIMAL(10, 2),
    FOREIGN KEY (examen_id) REFERENCES examenes(id),
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
    FOREIGN KEY (pregunta_id) REFERENCES preguntas(id),
    FOREIGN KEY (respuesta_id) REFERENCES respuestas(id)
);

-- Tabla de resultados de examenes
CREATE TABLE examenes_realizados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT,
    examen_id INT,
    puntaje_obtenido INT,
    fecha_entregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completado BOOL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
    FOREIGN KEY (examen_id) REFERENCES examenes(id)
);
ALTER TABLE examenes_realizados
MODIFY puntaje_obtenido INT;

DESCRIBE examenes_realizados;


-- Tabla de informes
CREATE TABLE solicitudes_de_aprobacion (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nombre_archivo VARCHAR(120) NOT NULL UNIQUE,
	solicitante_id INT,
	remitente_id INT,
	FOREIGN KEY (solicitante_id) REFERENCES maestros(id),
    FOREIGN KEY (remitente_id) REFERENCES usuarios(id)
);

select * from examenes;