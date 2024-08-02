from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from ..models.usuarios import Usuarios
from ..models.roles import Roles
from ..models.alumnos import Alumnos
from ..models.maestros import Maestros
from .. import db, bcrypt

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/auth/iniciarSesion', methods=['POST'])
def login():
    data = request.get_json()
    nombre = data.get('nombre')
    contrasena = data.get('contrasena')
    usuario = Usuarios.query.filter_by(nombre_usuario=nombre).first()
    if usuario and bcrypt.check_password_hash(usuario.contrasena, contrasena):
        login_user(usuario)
        
        id_adicional = None
        if usuario.rol_id == 1:
            alumno = Alumnos.query.filter_by(usuario_id=usuario.id).first()
            if alumno:
                id_adicional = alumno.id
        elif usuario.rol_id == 2:
            maestro = Maestros.query.filter_by(usuario_id=usuario.id).first()
            if maestro:
                id_adicional = maestro.id

        session['id_adicional'] = id_adicional

        return jsonify({'mensaje': 'Inicio de sesion exitoso', 'id_usuario': current_user.id, 'nombre': current_user.nombre_usuario, 'rol': current_user.rol_id, 'id_adicional': id_adicional}), 200
    else:
        return jsonify({'mensaje': 'Inicio de sesion fallido. Por favor revise usuario y contraseña'}), 401

@auth_bp.route('/auth/crearUsuario', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    nombre = datos.get('nombre')
    contrasena = datos.get('contrasena')
    if not nombre or not contrasena:
        return jsonify({'mensaje': 'Usuario y contraseña son requeridos'}), 400

    contrasena_encriptada = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    usuario = Usuarios(nombre_usuario=nombre, contrasena=contrasena_encriptada, rol_id=3)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado de forma exitosa'}), 201

@auth_bp.route('/auth/cerrarSesion', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('id_adicional', None)
    return jsonify({'mensaje': 'Cierre de sesion exitoso'}), 200

@auth_bp.route('/auth/usuarioActual', methods=['GET'])
@login_required
def usuario_actual():
    usuario = {
        'id_usuario': current_user.id,
        'nombre': current_user.nombre_usuario,
        'rol': current_user.rol_id,
        'id_adicional': session.get('id_adicional')
    }
    return jsonify(usuario), 200

@auth_bp.route('/auth/verificar', methods=['GET'])
def verificar():
    if current_user.is_authenticated:
        return jsonify({'logueado': True, 'rol': current_user.rol_id}), 200
    else:
        return jsonify({'logueado': False}), 200