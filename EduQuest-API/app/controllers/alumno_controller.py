from flask import Blueprint, request, jsonify
from ..models.alumnos import Alumnos
from .. import db
from datetime import datetime

alumno_bp = Blueprint('alumno_bp', __name__)

@alumno_bp.route('/Eduquest/alumnosBuscar', methods=['GET'])
def obtener_alumnos():

    alumno = Alumnos.query.all()

    return jsonify([{
        'id': m.id, 
        'usuario_id': m.usuario_id, 
        'nombres': m.nombres, 
        'apellidos': m.apellidos,
        'grado_id':m.grado_id,
        'especialidad_id':m.especialidad_id,
        'seccion_id':m.seccion_id,
        'created_at': m.created_at, 
        'updated_at': m.updated_at, 
        'deleted_at': m.deleted_at
        } for m in alumno])

@alumno_bp.route('/Eduquest/alumnosCrear', methods=['POST'])
def crear_alumnos():
  try: 
     
     data = request.get_json()

     nuevo_alumno = Alumnos(
        usuario_id=data['usuario_id'],
        nombres=data['nombres'],
        apellidos=data['apellidos'],
        grado_id=data['grado_id'],
        especialidad_id=data['especialidad_id'],
        seccion_id=data['seccion_id'],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None

     )

     db.session.add(nuevo_alumno)
     db.session.commit()

     return jsonify({
        'id': nuevo_alumno.id,
        'usuario_id': nuevo_alumno.usuario_id,
        'nombres': nuevo_alumno.nombres,
        'apellidos': nuevo_alumno.apellidos,
        'grado_id': nuevo_alumno.grado_id,
        'especialidad_id' : nuevo_alumno.especialidad_id,
        'seccion_id' : nuevo_alumno.seccion_id,
        'created_at': nuevo_alumno.created_at,
        'updated_at': nuevo_alumno.updated_at,
        'deleted_at': nuevo_alumno.deleted_at
     }), 201
  
  except Exception as e: 
     db.session.rollback()
     return jsonify ({'error': str(e)}), 500
  
@alumno_bp.route('/Eduquest/alumnosActualizar/<int:id>', methods=['PUT'])
def actualizar_alumnos(id):
   try: 
      

      
      data = request.get_json()

      alumnos = Alumnos.query.get_or_404(id)
      alumnos.usuario_id = data.get('usuario_id', alumnos.usuario_id)
      alumnos.nombres = data.get('nombres', alumnos.nombres)
      alumnos.apellidos = data.get('apellidos', alumnos.apellidos)
      alumnos.grado_id = data.get('grado_id', alumnos.grado_id)
      alumnos.especialidad_id = data.get('especialidad_id', alumnos.especialidad_id)
      alumnos.seccion_id = data.get('seccion_id', alumnos.seccion_id)
      alumnos.created_at = data.get('created_at', alumnos.created_at)
      alumnos.updated_at = data.get('update_at', alumnos.updated_at)
      alumnos.deleted_at = data.get('delete_at', alumnos.deleted_at)

      db.session.commit()

      return jsonify({
         'id': alumnos.id,
         'usuario_id': alumnos.usuario_id,
         'nombres': alumnos.nombres,
         'apellidos': alumnos.apellidos,
         'grado_id':alumnos.grado_id,
         'especialidad_id':alumnos.especialidad_id,
         'seccion_id':alumnos.seccion_id,
         'created_at': alumnos.created_at,
         'updated_at': alumnos.updated_at,
         'deleted_at': alumnos.deleted_at
      })
   except Exception as e:
      
      db.session.rollback()

      return jsonify({'error': str(e)}), 500
   
@alumno_bp.route('/Eduquest/alumnosEliminar/<int:id>', methods=['DELETE'])
def eliminar_alumnos(id):
   try: 
      
      alumno = Alumnos.query.get_or_404(id)

      db.session.delete(alumno)

      db.session.commit()
      return jsonify({'message': f'Alumno {id} fue eliminado con exito'})
   except Exception as e: 
      
      db.session.rollback()

      return jsonify({'error': str(e)}, 500)