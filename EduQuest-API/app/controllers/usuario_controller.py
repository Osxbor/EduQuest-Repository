from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from ..models.usuarios import Usuarios
from ..models.alumnos import Alumnos
from ..models.maestros import Maestros
from .. import db, bcrypt
from datetime import datetime

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/Eduquest/usuariosBuscar', methods=['GET'])
def buscar_usuarios():
    usuario = Usuarios.query.all()
    return jsonify([{
        'id': u.id, 
        'nombre_usuario': u.nombre_usuario, 
        'contrasena': u.contrasena,
        'rol_id': u.rol_id,
        'created_at': u.created_at, 
        'updated_at': u.updated_at, 
        'deleted_at': u.deleted_at
    } for u in usuario])

@usuario_bp.route('/Eduquest/usuariosBuscarPorId/<int:id>', methods=['GET'])
def buscar_usuario_por_id(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    usuario_data = {
        'id': usuario.id,
        'nombre_usuario': usuario.nombre_usuario,
        'contrasena': usuario.contrasena,
        'rol_id': usuario.rol_id,
        'created_at': usuario.created_at,
        'updated_at': usuario.updated_at,
        'deleted_at': usuario.deleted_at
    }

    if usuario.rol_id == 1:
        alumno = Alumnos.query.filter_by(usuario_id=usuario.id).first()
        if alumno:
            usuario_data.update({
                'nombres': alumno.nombres,
                'apellidos': alumno.apellidos,
                'grado_id': alumno.grado_id,
                'especialidad_id': alumno.especialidad_id,
                'seccion_id': alumno.seccion_id
            })
    elif usuario.rol_id == 2:
        maestro = Maestros.query.filter_by(usuario_id=usuario.id).first()
        if maestro:
            usuario_data.update({
                'nombres': maestro.nombres,
                'apellidos': maestro.apellidos
            })

    return jsonify(usuario_data), 200



@usuario_bp.route('/Eduquest/usuariosCrear', methods=['POST'])
def crear_usuario():
    try: 
        data = request.get_json()

        if 'nombre_usuario' not in data or 'contrasena' not in data or 'rol_id' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400

        contrasena_encriptada = bcrypt.generate_password_hash(data['contrasena']).decode('utf-8')

        nuevo_usuario = Usuarios(
            nombre_usuario=data['nombre_usuario'],
            contrasena=contrasena_encriptada,
            rol_id=data['rol_id'],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=None
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({
            'id': nuevo_usuario.id,
            'nombre_usuario': nuevo_usuario.nombre_usuario,
            'contrasena': nuevo_usuario.contrasena,
            'created_at': nuevo_usuario.created_at,
            'updated_at': nuevo_usuario.updated_at,
            'deleted_at': nuevo_usuario.deleted_at
        }), 201

    except Exception as e: 
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/Eduquest/usuariosActualizar/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    try: 
        data = request.get_json()

        usuario = Usuarios.query.get_or_404(id)
        usuario.nombre_usuario = data.get('nombre_usuario', usuario.nombre_usuario)

        if 'contrasena' in data:
            usuario.contrasena = bcrypt.generate_password_hash(data['contrasena']).decode('utf-8')

        usuario.rol_id = data.get('rol_id', usuario.rol_id)
        usuario.created_at = data.get('created_at', usuario.created_at)
        usuario.updated_at = datetime.now()
        usuario.deleted_at = data.get('deleted_at', usuario.deleted_at)

        db.session.commit()

        return jsonify({
            'id': usuario.id,
            'nombre_usuario': usuario.nombre_usuario,
            'contrasena': usuario.contrasena,
            'rol_id': usuario.rol_id,
            'created_at': usuario.created_at,
            'updated_at': usuario.updated_at,
            'deleted_at': usuario.deleted_at
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/Eduquest/usuariosEliminar/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    try: 
        usuario = Usuarios.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': f'Usuario {id} fue eliminado con exito'})
    except Exception as e: 
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/Eduquest/usuarioAdminExiste', methods=['GET'])
def usuario_admin_existe():
    existe_admin = Usuarios.query.filter_by(rol_id=3).first() is not None
    return jsonify({'existe': existe_admin})