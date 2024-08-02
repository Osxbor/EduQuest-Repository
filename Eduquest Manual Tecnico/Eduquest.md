# Manual Tecnico - EDUQUEST
No Yawning, Pure learning
## Introducción

Eduques es una pagina web diseñada para gestionar la creacion de examenes, evaluacion de alumnos de forma virtual. Creada para poder serimplementada dentro de cualquier centro educativo. Este manual técnico proporciona informacion detallada sobre la arquitectura, tecnologias y configuraciones necesarias para implementar y mantener el sistema EDUQUEST

## Arquitectura del Sistema
El sistema de EDUQUEST esta formado por tres componentes principales 
1. **Backend**: Desarrollado Utilizando el framework Flask.
2. **Frontend**: Desarrollado utilizando un framework JavaScript: Astro
3. **Gestor de Datos**: Utiliza una base de datos SQLAlchemy.


## Requisitos Técnicos
1. **Backend**: Python, Flask, WTForms, Flask-Login, Werkzeug,Flask-Bcrypt
2. **Frontend**: Angular, React o Vue
3. **Gestión de Datos**: Archivos JSON



## Estructura de Datos a Almacenar en JSON
### Ejemplo de Estructura de Roles
```json
{
    "Roles": [
       {
         "id": "nuevo_rol.id",
         "nombre": "nuevo_rol.nombre",
         "created_at": "nuevo_rol.created_at",
         "updated_at": "nuevo_rol.updated_at",
         "deleted_at": "nuevo_rol.deleted_at"
       }
    ]
}
```
### Ejemplo de Estructura de Usuarios
```json
{
    "Usuarios": [
       {
         "id": "nuevo_usuario.id",
         "nombre_usuario": "nuevo_usuario.nombre_usuario",
         "contrasena": "nuevo_usuario.contrasena",
         "created_at": "nuevo_usuario.created_at",
         "updated_at": "nuevo_usuario.updated_at",
          "deleted_at": "nuevo_usuario.deleted_at"
       }
    ]
}
```



## Implementación del Backend
### Configuración del Entorno
1. Instalar Flask, Python y pip (si no se instalo con las variables del sistema).
2. Configurar un nuevo proyecto con pip init.
3. Instalar dependencias el resto de herramientas necesarias.

### Ejemplo de model
Model Usuarios.py

![Mi Imagen](model%20ejemplo.png)

### Ejemplo de Controller
Controller Usuario_controller.py

![Mi Imagen](/controller%20ejemplo.png)

## Implementación del Frontend
### Configuración del Entorno
1. Instalar Astro
3. Configurar los servicios y componentes 
### Ejemplo de Configuración en Angular
1. Instalar Astro
2. Instalar extenciones
3. Configurar componentes y servicios 



## Capturas de Pantalla y Descripcion

### Funciones del administrador

Inicio de secion de administrador
![Mi Imagen](/Admin.png)

Añadir secciones-Administrador
![Añadir Ssecciones](/Secciones.png)

Añadir Grados-Administrados
![Añadir Grados](/grados.png)

Añadir Secciones-Administrador
![Añadir Ssecciones](/Agregar%20Usuarios.png)

Aprobar examen-Administrados
![Aprobar examen](/AprobarExamen.png)



### Funciones del Maestro

Inicio de Sesion maestro
![Inicio de SEcion MAestro](/InicioMaestro.png)

Crear Examen-Maestro
![Crear examen](/Crear%20Examen.png)


### Funciones del Alumno

Inicio de Sesion Alumno
![Inicio de SEcion MAestro](/Inicio-Alumno.png)

Contestar Examenes 
![Crear examen](/ExamenesAlumno.png)

Puede crear un pdf con sus respuestas
![Añadir Ssecciones](/pdf.png)