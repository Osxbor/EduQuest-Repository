from flask import Blueprint, request, jsonify
from ..models.grado import Grados
from .. import db
from datetime import datetime

grado_bp = Blueprint('grado_bp', __name__)

@grado_bp.route('/Eduquest/gradosBuscar', methods=['GET'])
def buscar_grados():
    grados = Grados.query.all()
    return jsonify([{
        'id': g.id,
        'nombre': g.nombre,
        'created_at': g.created_at,
        'updated_at': g.updated_at,
        'deleted_at': g.deleted_at
    } for g in grados])

@grado_bp.route('/Eduquest/gradosCrear', methods=['POST'])
def crear_grado():
    try:
        data = request.get_json()
        nuevo_grado = Grados(
            nombre=data['nombre'],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=None
        )
        db.session.add(nuevo_grado)
        db.session.commit()
        return jsonify({
            'id': nuevo_grado.id,
            'nombre': nuevo_grado.nombre,
            'created_at': nuevo_grado.created_at,
            'updated_at': nuevo_grado.updated_at,
            'deleted_at': nuevo_grado.deleted_at
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grado_bp.route('/Eduquest/gradosActualizar/<int:id>', methods=['PUT'])
def actualizar_grado(id):
    try:
        data = request.get_json()
        grado = Grados.query.get_or_404(id)
        grado.nombre = data.get('nombre', grado.nombre)
        grado.updated_at = datetime.now()
        grado.deleted_at = data.get('deleted_at', grado.deleted_at)
        db.session.commit()
        return jsonify({
            'id': grado.id,
            'nombre': grado.nombre,
            'created_at': grado.created_at,
            'updated_at': grado.updated_at,
            'deleted_at': grado.deleted_at
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grado_bp.route('/Eduquest/gradosEliminar/<int:id>', methods=['DELETE'])
def eliminar_grado(id):
    try:
        grado = Grados.query.get_or_404(id)
        db.session.delete(grado)
        db.session.commit()
        return jsonify({'message': f'Grado {id} fue eliminado con éxito'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500