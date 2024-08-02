CREATE DATABASE DataBaseEduquest;
use DataBaseEduquest;
-- Tabla de roles
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

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

-- Tabla de alumnos
CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    clave INT NOT NULL,
    grado_id INT,
    correo VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (grado_id) REFERENCES grados(id)
);

-- Tabla de maestros
CREATE TABLE maestros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100) NOT NULL,
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

-- Relación entre maestros, grados y materias
CREATE TABLE maestro_grados_materias (
    maestro_id INT,
    grado_id INT,
    materia_id INT,
    PRIMARY KEY (maestro_id, grado_id, materia_id),
    FOREIGN KEY (maestro_id) REFERENCES maestros(id),
    FOREIGN KEY (grado_id) REFERENCES grados(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);

-- Relación entre grados y materias
CREATE TABLE grado_materias (
    grado_id INT,
    materia_id INT,
    PRIMARY KEY (grado_id, materia_id),
    FOREIGN KEY (grado_id) REFERENCES grados(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
);


-- Tabla de examenes
CREATE TABLE examenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    grado_id INT,
    materia_id INT,
    cantidad_preguntas INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (grado_id) REFERENCES grados(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id)
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
    es_correcta BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (pregunta_id) REFERENCES preguntas(id)
);

-- Tabla intermedia de examen, pregunta y respuesta
CREATE TABLE examen_pregunta_respuesta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    examen_id INT,
    pregunta_id INT,
    respuesta_id INT,
    FOREIGN KEY (examen_id) REFERENCES examenes(id),
    FOREIGN KEY (pregunta_id) REFERENCES preguntas(id),
    FOREIGN KEY (respuesta_id) REFERENCES respuestas(id)
);

-- Tabla de resultados de examenes
CREATE TABLE resultados_examenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT,
    examen_id INT,
    puntaje_obtenido INT NOT NULL,
    fecha_realizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
    FOREIGN KEY (examen_id) REFERENCES examenes(id)
);

SELECT * FROM grados;
SELECT * FROM materias;
