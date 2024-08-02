from flask import Blueprint
from .controllers.alumno_controller import alumno_bp
from .controllers.especialidad_controller import especialidad_bp
from .controllers.examen_controller import examen_bp
from .controllers.examen_resuelto_controller import examen_resuelto_bp
from .controllers.grado_controlador import grado_bp
from .controllers.maestro_controller import maestro_bp
from .controllers.materia_controller import materia_bp
from .controllers.pregunta_controller import pregunta_bp
from .controllers.respuesta_controller import respuesta_bp
from .controllers.rol_controller import rol_bp
from .controllers.seccion_controller import seccion_bp
from .controllers.usuario_controller import usuario_bp
from .controllers.auth import auth_bp
from .controllers.asignacion_controller import asignacion_bp
from .controllers.buscar_controller import Busqueda_bp
from .controllers.examen_filtros_controller import ExamenesFiltros_bp
from .controllers.responder_examen import responder_bp
main_bp = Blueprint('main_bp', __name__)
# Registramos todas las blueprints que importamos para que sean reconocibles para el sistema
def register_blueprints(app):
    app.register_blueprint(alumno_bp)
    app.register_blueprint(especialidad_bp)
    app.register_blueprint(examen_bp)
    app.register_blueprint(examen_resuelto_bp)
    app.register_blueprint(grado_bp)
    app.register_blueprint(maestro_bp)
    app.register_blueprint(materia_bp)
    app.register_blueprint(pregunta_bp)
    app.register_blueprint(respuesta_bp)
    app.register_blueprint(rol_bp)
    app.register_blueprint(seccion_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(auth_bp)    
    app.register_blueprint(asignacion_bp)
    app.register_blueprint(Busqueda_bp)
    app.register_blueprint(ExamenesFiltros_bp)
    app.register_blueprint(responder_bp)