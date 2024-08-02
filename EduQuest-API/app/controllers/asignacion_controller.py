from flask import Blueprint, request, jsonify
from ..models.maestros import Maestros
from ..models.grado import Grados
from ..models.especialidades import Especialidades
from ..models.secciones import Secciones
from ..models.materias import Materias
from ..models.asignacionMaestros import Asignaciones
from .. import db
from datetime import datetime

asignacion_bp = Blueprint('asignacion_bp', __name__)

@asignacion_bp.route('/Eduquest/asignacionesBuscar', methods=['GET'])
def buscar_asignaciones():
    asignaciones = Asignaciones.query.filter_by(deleted_at=None).all()
    return jsonify([{
        'id': a.id,
        'maestro': {
            'id': a.maestro.id,
            'nombre': f'{a.maestro.nombres} {a.maestro.apellidos}'
        },
        'grado': {
            'id': a.grado.id,
            'nombre': a.grado.nombre
        },
        'especialidad': {
            'id': a.especialidad.id,
            'nombre': a.especialidad.nombre
        },
        'seccion': {
            'id': a.seccion.id,
            'nombre': a.seccion.nombre
        },
        'materia': {
            'id': a.materia.id,
            'nombre': a.materia.nombre
        },
        'created_at': a.created_at,
        'updated_at': a.updated_at,
        'deleted_at': a.deleted_at
    } for a in asignaciones])

@asignacion_bp.route('/Eduquest/asignacionesCrear', methods=['POST'])
def crear_asignacion():
    try:
        data = request.get_json()
        nueva_asignacion = Asignaciones(
            maestro_id=data['maestro_id'],
            grado_id=data['grado_id'],
            especialidad_id=data['especialidad_id'],
            seccion_id=data['seccion_id'],
            materia_id=data['materia_id'],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=None
        )

        db.session.add(nueva_asignacion)
        db.session.commit()

        return jsonify({
            'id': nueva_asignacion.id,
            'maestro_id': nueva_asignacion.maestro_id,
            'grado_id': nueva_asignacion.grado_id,
            'especialidad_id': nueva_asignacion.especialidad_id,
            'seccion_id': nueva_asignacion.seccion_id,
            'materia_id': nueva_asignacion.materia_id,
            'created_at': nueva_asignacion.created_at,
            'updated_at': nueva_asignacion.updated_at,
            'deleted_at': nueva_asignacion.deleted_at
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@asignacion_bp.route('/Eduquest/asignacionesActualizar/<int:id>', methods=['PUT'])
def actualizar_asignacion(id):
    try:
        data = request.get_json()
        asignacion = Asignaciones.query.get_or_404(id)
        asignacion.maestro_id = data.get('maestro_id', asignacion.maestro_id)
        asignacion.grado_id = data.get('grado_id', asignacion.grado_id)
        asignacion.especialidad_id = data.get('especialidad_id', asignacion.especialidad_id)
        asignacion.seccion_id = data.get('seccion_id', asignacion.seccion_id)
        asignacion.materia_id = data.get('materia_id', asignacion.materia_id)
        asignacion.updated_at = datetime.now()

        db.session.commit()

        return jsonify({
            'id': asignacion.id,
            'maestro_id': asignacion.maestro_id,
            'grado_id': asignacion.grado_id,
            'especialidad_id': asignacion.especialidad_id,
            'seccion_id': asignacion.seccion_id,
            'materia_id': asignacion.materia_id,
            'created_at': asignacion.created_at,
            'updated_at': asignacion.updated_at,
            'deleted_at': asignacion.deleted_at
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@asignacion_bp.route('/Eduquest/asignacionesEliminar/<int:id>', methods=['DELETE'])
def eliminar_asignacion(id):
    try:
        asignacion = Asignaciones.query.get_or_404(id)
        asignacion.deleted_at = datetime.now()
        db.session.commit()
        return jsonify({'message': f'Asignación {id} fue marcada como eliminada exitosamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
