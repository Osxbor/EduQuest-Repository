from flask import Blueprint, request, jsonify
from ..models.alumnos import Alumnos
from ..models.examenes import Examenes
from ..models.grado import Grados
from ..models.maestros import Maestros
from ..models.preguntas import Preguntas
from ..models.roles import Roles
from ..models.secciones import Secciones
from ..models.respuestas import Respuestas
from ..models.usuarios import Usuarios
from ..models.materias import Materias
from ..models.especialidades import Especialidades
from .. import db
from datetime import datetime

Busqueda_bp = Blueprint('Busqueda_bp', __name__)

def obtener_modelo_por_nombre(nombre_tabla):
    models = {
        'alumnos': Alumnos,
        'examenes': Examenes,
        'grados': Grados,
        'maestros': Maestros,
        'preguntas': Preguntas,
        'secciones': Secciones,
        'respuestas': Respuestas,
        'materias': Materias,
        'usuarios': Usuarios,
        'roles': Roles,
        'especialidades': Especialidades
    }
    return models.get(nombre_tabla.lower())

@Busqueda_bp.route('/Buscar/<nombre_tabla>', methods=['GET'])
def obtener_todos(nombre_tabla):
    modelo = obtener_modelo_por_nombre(nombre_tabla)
    if modelo is None:
        return jsonify({'error': f"Tabla {nombre_tabla} no se encontro."}), 404

    registros = modelo.query.all()
    resultado = [registro.to_dict() for registro in registros]
    return jsonify(resultado), 200

@Busqueda_bp.route('/Buscar/<nombre_tabla>/<int:registro_id>', methods=['GET'])
def obtener_por_id(nombre_tabla, registro_id):
    modelo = obtener_modelo_por_nombre(nombre_tabla)
    if modelo is None:
        return jsonify({'error': f"Tabla {nombre_tabla} no encontrada."}), 404

    registro = modelo.query.get(registro_id)
    if registro is None:
        return jsonify({'error': f"Registro con el id: {registro_id} no se ha encontrado en la tabla: {nombre_tabla}."}), 404

    return jsonify(registro.to_dict()), 200