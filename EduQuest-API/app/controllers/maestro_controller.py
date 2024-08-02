from flask import Blueprint, request, jsonify
from ..models.maestros import Maestros
from .. import db
from datetime import datetime

maestro_bp = Blueprint('maestro_bp', __name__)

@maestro_bp.route('/Eduquest/maestrosBuscar', methods=['GET'])
def buscar_maestros():

    maestro = Maestros.query.all()

    return jsonify([{
        'id': m.id, 
        'usuario_id': m.usuario_id, 
        'nombres': m.nombres, 
        'apellidos': m.apellidos, 
        'created_at': m.created_at, 
        'updated_at': m.updated_at, 
        'deleted_at': m.deleted_at
        } for m in maestro])

@maestro_bp.route('/Eduquest/maestrosCrear', methods=['POST'])
def crear_maestro():
  try: 
     
     data = request.get_json()

     nuevo_maestro = Maestros(
        usuario_id=data['usuario_id'],
        nombres=data['nombres'],
        apellidos=data['apellidos'],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None

     )

     db.session.add(nuevo_maestro)
     db.session.commit()

     return jsonify({
        'id': nuevo_maestro.id,
        'usuario_id': nuevo_maestro.usuario_id,
        'nombres': nuevo_maestro.nombres,
        'apellidos': nuevo_maestro.apellidos,
        'created_at': nuevo_maestro.created_at,
        'updated_at': nuevo_maestro.updated_at,
        'deleted_at': nuevo_maestro.deleted_at
     }), 201
  
  except Exception as e: 
     db.session.rollback()
     return jsonify ({'error': str(e)}), 500
  
@maestro_bp.route('/Eduquest/maestrosActualizar/<int:id>', methods=['PUT'])
def actualizar_maestro(id):
   try: 
      

      
      data = request.get_json()

      maestro = Maestros.query.get_or_404(id)
      maestro.usuario_id = data.get('usuario_id', maestro.usuario_id)
      maestro.nombres = data.get('nombres', maestro.nombres)
      maestro.apellidos = data.get('apellidos', maestro.apellidos)
      maestro.created_at = data.get('created_at', maestro.created_at)
      maestro.updated_at = data.get('update_at', maestro.updated_at)
      maestro.deleted_at = data.get('delete_at', maestro.deleted_at)

      db.session.commit()

      return jsonify({
         'id': maestro.id,
         'usuario_id': maestro.usuario_id,
         'nombres': maestro.nombres,
         'apellidos': maestro.apellidos,
         'created_at': maestro.created_at,
         'updated_at': maestro.updated_at,
         'deleted_at': maestro.deleted_at
      })
   except Exception as e:
      
      db.session.rollback()

      return jsonify({'error': str(e)}), 500
   
@maestro_bp.route('/Eduquest/maestrosEliminar/<int:id>', methods=['DELETE'])
def eliminar_maestro(id):
   try: 
      
      maestro = Maestros.query.get_or_404(id)

      db.session.delete(maestro)

      db.session.commit()
      return jsonify({'message': f'Maestro {id} fue eliminado con exito'})
   except Exception as e: 
      
      db.session.rollback()

      return jsonify({'error': str(e)}, 500)
