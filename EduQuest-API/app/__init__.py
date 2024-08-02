from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    CORS(app)

    # Importa los modelos y blueprints dentro del contexto de la app
    with app.app_context():
        from .models.grado import Grados
        from .models.alumnos import Alumnos
        from .models.asignacionMaestros import Asignaciones
        from .models.especialidades import Especialidades
        from .models.examenes_resueltos import ExamenesResueltos
        from .models.examenes import Examenes
        from .models.maestros import Maestros
        from .models.materias import Materias
        from .models.preguntas import Preguntas
        from .models.respuestas import Respuestas
        from .models.roles import Roles
        from .models.secciones import Secciones
        from .models.usuarios import Usuarios

        # Registrar blueprints
        from .routes import register_blueprints
        register_blueprints(app)

        # Crear todas las tablas
        db.create_all()
    
    return app
