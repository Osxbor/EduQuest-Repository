from flask import Blueprint, request, jsonify
from ..models.examenes_resueltos import ExamenesResueltos
from ..models.preguntas_respondidas import PreguntaRespondida
from ..models.examenes import Examenes
from ..models.usuarios import Usuarios
from ..models.alumnos import Alumnos
from .. import db
from datetime import datetime

examen_resuelto_bp = Blueprint('examen_resuelto_bp', __name__)

@examen_resuelto_bp.route('/Eduquest/ER_Buscar', methods=['GET'])
def buscar_ER():
    examenes_resueltos = ExamenesResueltos.query.all()
    return jsonify([examen_resuelto.to_dict() for examen_resuelto in examenes_resueltos])
@examen_resuelto_bp.route('/Eduquest/ER_BuscarPorID/<int:id>', methods=['GET'])
def buscar_ER_por_id(id):
    examen_resuelto = ExamenesResueltos.query.get_or_404(id)
    
    # Obtener el ID del examen
    examen_id = examen_resuelto.examen_id
    
    # Buscar todos los alumnos que tienen asignado el examen y lo han completado
    alumnos_con_examen = ExamenesResueltos.query.filter_by(examen_id=examen_id, completado=True).all()
    
    # Verificar la cantidad de alumnos encontrados
    print(f"Total de alumnos con el examen completado: {len(alumnos_con_examen)}")
    
    # Convertir los resultados en un formato serializable
    alumnos_lista = []
    for alumno in alumnos_con_examen:
        alumno_info = Alumnos.query.filter_by(id=alumno.alumno_id).first()
        
        if alumno_info:
            alumnos_lista.append({
                'alumno_id': alumno.alumno_id,
                'nombres': alumno_info.nombres,
                'apellidos': alumno_info.apellidos,
                'puntaje_obtenido': alumno.puntaje_obtenido,
                'completado': alumno.completado,
                'fecha_entregado': alumno.fecha_entregado.strftime('%Y-%m-%d') if alumno.fecha_entregado else None
            })
        else:
            print(f"Información del alumno no encontrada para alumno_id: {alumno.alumno_id}")
    
    # Verificar la lista de alumnos generada
    print(f"Total de alumnos en la lista final: {len(alumnos_lista)}")
    
    return jsonify({
        'examen_resuelto': examen_resuelto.to_dict(),
        'alumnos': alumnos_lista
    })






@examen_resuelto_bp.route('/Eduquest/ER_Crear', methods=['POST'])
def crear_ER():
    try:
        data = request.get_json()

        alumno_id = data['alumno_id']
        examen_id = data['examen_id']

        examen = Examenes.query.get(examen_id)
        if not examen:
            return jsonify({'error': 'Examen no encontrado'}), 404

        total_preguntas = examen.cantidad_preguntas
        respondidas = PreguntaRespondida.query.filter_by(examen_id=examen_id, alumno_id=alumno_id).count()

        if respondidas == total_preguntas:
            completado = True
        else:
            completado = False

        puntaje_obtenido = db.session.query(db.func.sum(PreguntaRespondida.puntos_obtenidos)).filter_by(examen_id=examen_id, alumno_id=alumno_id).scalar()
        
        nuevo_examen_resuelto = ExamenesResueltos(
            alumno_id=alumno_id,
            examen_id=examen_id,
            puntaje_obtenido=puntaje_obtenido,
            completado=completado,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=None
        )
        
        db.session.add(nuevo_examen_resuelto)
        db.session.commit()

        return jsonify(nuevo_examen_resuelto.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@examen_resuelto_bp.route('/Eduquest/ER_Actualizar/<int:id>', methods=['PUT'])
def actualizar_ER(id):
    try:
        data = request.get_json()
        examen_resuelto = ExamenesResueltos.query.get_or_404(id)

        examen_resuelto.alumno_id = data.get('alumno_id', examen_resuelto.alumno_id)
        examen_resuelto.examen_id = data.get('examen_id', examen_resuelto.examen_id)
        examen_resuelto.puntaje_obtenido = data.get('puntaje_obtenido', examen_resuelto.puntaje_obtenido)
        examen_resuelto.completado = data.get('completado', examen_resuelto.completado)
        examen_resuelto.updated_at = datetime.now()
        examen_resuelto.deleted_at = data.get('deleted_at', examen_resuelto.deleted_at)

        db.session.commit()
        return jsonify(examen_resuelto.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@examen_resuelto_bp.route('/Eduquest/ER_Eliminar/<int:id>', methods=['DELETE'])
def eliminar_ER(id):
    try:
        examen_resuelto = ExamenesResueltos.query.get_or_404(id)
        db.session.delete(examen_resuelto)
        db.session.commit()
        return jsonify({'message': f'ExamenResuelto {id} fue eliminado con éxito'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@examen_resuelto_bp.route('/Eduquest/ER_Buscar_Filtros/<int:alumno_id>', methods=['GET'])
def obtener_examenes_realizados(alumno_id):
    try:
        completado = request.args.get('completado', type=int)
        fecha_entregado = request.args.get('fecha_entregado')
        
        # Construir la consulta
        query = ExamenesResueltos.query.filter_by(alumno_id=alumno_id)
        
        if completado is not None:
            query = query.filter_by(completado=bool(completado))
        
        if fecha_entregado:
            try:
                fecha_entregado_dt = datetime.strptime(fecha_entregado, '%Y-%m-%d')
                query = query.filter(ExamenesResueltos.fecha_entregado >= fecha_entregado_dt)
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido, se espera YYYY-MM-DD'}), 400
        
        examenes_realizados = query.all()
        
        # Convertir los resultados en un formato serializable
        resultados = []
        for examen in examenes_realizados:
            examen_detalle = Examenes.query.get(examen.examen_id)
            if examen_detalle:
                resultados.append({
                    'id': examen.id,
                    'alumno_id': examen.alumno_id,
                    'examen_id': examen.examen_id,
                    'nombre_examen': examen_detalle.nombre_examen,
                    'puntaje_total': examen_detalle.puntaje_total,
                    'puntaje_obtenido': examen.puntaje_obtenido,
                    'fecha_entregado': examen.fecha_entregado.strftime('%Y-%m-%d') if examen.fecha_entregado else None,
                    'completado': examen.completado
                })
        
        return jsonify(resultados), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@examen_resuelto_bp.route('/Eduquest/ER_Buscar_Filtros_NoEntregado/<int:alumno_id>', methods=['GET'])
def obtener_examenes_realizados_fecha(alumno_id):
    try:
        completado = request.args.get('completado', type=int)
        fecha_entregado = request.args.get('fecha_entregado')
        
        # Obtener la fecha actual sin la parte de tiempo
        fecha_actual = datetime.now().date()
        
        # Construir la consulta
        query = ExamenesResueltos.query.join(Examenes, ExamenesResueltos.examen_id == Examenes.id).filter(
            ExamenesResueltos.alumno_id == alumno_id,
            Examenes.fecha_entrega < fecha_actual
        )
        
        if completado is not None:
            query = query.filter(ExamenesResueltos.completado == bool(completado))
        
        if fecha_entregado:
            try:
                fecha_entregado_dt = datetime.strptime(fecha_entregado, '%Y-%m-%d').date()
                query = query.filter(ExamenesResueltos.fecha_entregado < fecha_entregado_dt)
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido, se espera YYYY-MM-DD'}), 400
        
        examenes_realizados = query.all()
        
        # Convertir los resultados en un formato serializable
        resultados = []
        for examen_resuelto in examenes_realizados:
            examen = Examenes.query.get(examen_resuelto.examen_id)
            if examen:
                resultados.append({
                    'id': examen_resuelto.id,
                    'alumno_id': examen_resuelto.alumno_id,
                    'examen_id': examen_resuelto.examen_id,
                    'nombre_examen': examen.nombre_examen,
                    'puntaje_total': examen.puntaje_total,
                    'puntaje_obtenido': examen_resuelto.puntaje_obtenido,
                    'fecha_entrega': examen.fecha_entrega.strftime('%Y-%m-%d') if examen.fecha_entrega else None,
                    'completado': examen_resuelto.completado
                })
        
        return jsonify(resultados), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


    

@examen_resuelto_bp.route('/Eduquest/ER_Buscar_Filtros_fecha/<int:alumno_id>', methods=['GET'])
def obtener_examenes_no_realizados(alumno_id):
    try:
        completado = request.args.get('completado', type=int)
        fecha_entregado = request.args.get('fecha_entregado')
        
        # Obtener la fecha actual sin la parte de tiempo
        fecha_actual = datetime.now().date()
        
        # Construir la consulta
        query = ExamenesResueltos.query.join(Examenes, ExamenesResueltos.examen_id == Examenes.id).filter(
            ExamenesResueltos.alumno_id == alumno_id,
            Examenes.fecha_entrega >= fecha_actual
        )
        
        if completado is not None:
            query = query.filter(ExamenesResueltos.completado == bool(completado))
        
        if fecha_entregado:
            try:
                fecha_entregado_dt = datetime.strptime(fecha_entregado, '%Y-%m-%d').date()
                query = query.filter(ExamenesResueltos.fecha_entregado >= fecha_entregado_dt)
            except ValueError:
                return jsonify({'error': 'Formato de fecha inválido, se espera YYYY-MM-DD'}), 400
        
        examenes_realizados = query.all()
        
        # Convertir los resultados en un formato serializable
        resultados = []
        for examen_resuelto in examenes_realizados:
            examen = Examenes.query.get(examen_resuelto.examen_id)
            if examen:
                resultados.append({
                    'id': examen_resuelto.id,
                    'alumno_id': examen_resuelto.alumno_id,
                    'examen_id': examen_resuelto.examen_id,
                    'nombre_examen': examen.nombre_examen,
                    'puntaje_total': examen.puntaje_total,
                    'puntaje_obtenido': examen_resuelto.puntaje_obtenido,
                    'fecha_entrega': examen.fecha_entrega.strftime('%Y-%m-%d') if examen.fecha_entrega else None,
                    'completado': examen_resuelto.completado
                })
        
        return jsonify(resultados), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
