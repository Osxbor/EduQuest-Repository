from flask import Blueprint, request, jsonify
from ..models.roles import Roles
from .. import db
from datetime import datetime

rol_bp = Blueprint('rol_bp', __name__)

@rol_bp.route('/Eduquest/rolesBuscar', methods=['GET'])
def buscar_roles():
    roles = Roles.query.all()
    return jsonify([{
        'id': r.id,
        'nombre': r.nombre,
        'created_at': r.created_at,
        'updated_at': r.updated_at,
        'deleted_at': r.deleted_at
    } for r in roles])

@rol_bp.route('/Eduquest/rolesCrear', methods=['POST'])
def crear_roles():
    try:
        data = request.get_json()
        nuevo_rol = Roles(
            nombre=data['nombre'],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=None
        )
        db.session.add(nuevo_rol)
        db.session.commit()
        return jsonify({
            'id': nuevo_rol.id,
            'nombre': nuevo_rol.nombre,
            'created_at': nuevo_rol.created_at,
            'updated_at': nuevo_rol.updated_at,
            'deleted_at': nuevo_rol.deleted_at
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@rol_bp.route('/Eduquest/rolesActualizar/<int:id>', methods=['PUT'])
def actualizar_rol(id):
    try:
        data = request.get_json()
        roles = Roles.query.get_or_404(id)
        roles.nombre = data.get('nombre', Roles.nombre)
        roles.updated_at = datetime.now()
        roles.deleted_at = data.get('deleted_at', roles.deleted_at)
        db.session.commit()
        return jsonify({
            'id': roles.id,
            'nombre': roles.nombre,
            'created_at': roles.created_at,
            'updated_at': roles.updated_at,
            'deleted_at': roles.deleted_at
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@rol_bp.route('/Eduquest/rolesEliminar/<int:id>', methods=['DELETE'])
def eliminar_rol(id):
    try:
        roles = Roles.query.get_or_404(id)
        db.session.delete(Roles)
        db.session.commit()
        return jsonify({'message': f'Rol {id} fue eliminado con éxito'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500