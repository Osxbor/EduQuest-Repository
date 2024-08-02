from flask import Blueprint, request, jsonify
from ..models.examenes import Examenes
from ..models.examenes_resueltos import ExamenesResueltos
from ..models.preguntas_respondidas import PreguntaRespondida
from ..models.preguntas import Preguntas
from ..models.respuestas import Respuestas
from ..models.alumnos import Alumnos
from ..models.especialidades import Especialidades
from ..models.materias import Materias
from ..models.secciones import Secciones
from ..models.grado import Grados

from flask import send_file
import io
from reportlab.pdfgen import canvas

from .. import db
from datetime import datetime

examen_bp = Blueprint('examen_bp', __name__)

#@app.route() es un DECORADOR que define la ruta en la que se puede encontrar la función, en este caso, buscar_examenes().
#methods es un PARAMETRO para definir qué método HTTP puede usar la ruta que se especifíca en el DECORADOR
@examen_bp.route('/Eduquest/examenesBuscar', methods=['GET'])
def buscar_examenes():

    #Se utiliza el modelo Examenes
    #all() está recuperando todos los registros de la tabla que está asociada al modelo Examenes
    #examen va a ser una lista de objetos, estos objetos representarán un registro en la tabla examenes
    examen = Examenes.query.all()

    #'for g in examen' es un BUCLE DE LA COMPRESIÓN DE LISTA. 'lista' es una lista que contiene los registros de la base de datos,
    # esta compresión de lista itera sobre cada objeto g. Para cada objeto crea un diccionario que mapea los atributos a sus respectivos valores de 'g'.
    # en la lista, cada elemento 'g' es un OBJETO que represnta un solo examen.
    #josonify() convierte el objeto Pyhton (lo que está dentro de sus paréntesis, es decir, 
    # la lista de dicciionarios) en una respuesta .JSON
    return jsonify([{
        'id': g.id, 
        'nombre_examen': g.nombre_examen, 
        'grado_id': g.grado_id, 
        'materia_id': g.materia_id,
        'especialidad_id': g.especialidad_id,
        'seccion_id': g.seccion_id,
        'cantidad_preguntas': g.cantidad_preguntas,
        'fecha_publicacion': g.fecha_publicacion,
        'fecha_entrega': g.fecha_entrega,
        'estado': g.estado,
        'aproved': g.aproved,
        'comentario': g.comentario,
        'created_at': g.created_at, 
        'updated_at': g.updated_at, 
        'deleted_at': g.deleted_at
        } for g in examen])



@examen_bp.route('/Eduquest/examenesBuscarPorID/<int:id>', methods=['GET'])
def buscar_examenes_por_id(id):
    
    examen = Examenes.query.get_or_404(id)
    
    return jsonify({
        'id': examen.id, 
        'nombre_examen': examen.nombre_examen, 
        'grado_id': examen.grado_id, 
        'materia_id': examen.materia_id, 
        'especialidad_id': examen.especialidad_id,
        'seccion_id': examen.seccion_id,
        'cantidad_preguntas': examen.cantidad_preguntas,
        'puntaje_total': examen.puntaje_total,
        'fecha_publicacion': examen.fecha_publicacion,
        'fecha_entrega': examen.fecha_entrega,
        'estado': examen.estado,
        'aproved': examen.aproved,
        'comentario': examen.comentario,
        'created_at': examen.created_at, 
        'updated_at': examen.updated_at, 
        'deleted_at': examen.deleted_at
    })

@examen_bp.route('/Eduquest/examenesBuscarPorFiltros', methods=['GET'])
def buscar_examenes_por_filtros():
    # Obtener parámetros de la URL
    id = request.args.get('id')
    nombre_examen = request.args.get('nombre_examen')
    grado_id = request.args.get('grado_id')
    materia_id = request.args.get('materia_id')
    especialidad_id = request.args.get('especialidad_id')
    seccion_id = request.args.get('seccion_id')
    cantidad_preguntas = request.args.get('cantidad_preguntas')
    fecha_publicacion = request.args.get('fecha_publicacion')
    fecha_entrega = request.args.get('fecha_entrega')
    estado = request.args.get('estado')
    aproved = request.args.get('aproved')
    comentario = request.args.get('comentario')
    created_at = request.args.get('created_at')
    updated_at = request.args.get('updated_at')
    deleted_at = request.args.get('deleted_at')
    
    # Crear una consulta base
    query = Examenes.query
    
    # Agregar filtros a la consulta si los parámetros están presentes
    if id:
        query = query.filter_by(id=id)
    if nombre_examen:
        query = query.filter_by(nombre_examen=nombre_examen)
    if grado_id:
        query = query.filter_by(grado_id=grado_id)
    if materia_id:
        query = query.filter_by(materia_id=materia_id)
    if especialidad_id:
        query = query.filter_by(especialidad_id=especialidad_id)
    if seccion_id:
        query = query.filter_by(seccion_id=seccion_id)
    if cantidad_preguntas:
        query = query.filter_by(cantidad_preguntas=cantidad_preguntas)
    if fecha_publicacion:
        query = query.filter_by(fecha_publicacion=fecha_publicacion)
    if fecha_entrega:
        query = query.filter_by(fecha_entrega=fecha_entrega)
    if estado:
        query = query.filter_by(estado=estado)
    if aproved:
        query = query.filter_by(aproved=aproved)
    if comentario:
        query = query.filter_by(comentario=comentario)
    if created_at:
        query = query.filter_by(created_at=created_at)
    if updated_at:
        query = query.filter_by(updated_at=updated_at)
    if deleted_at:
        query = query.filter_by(deleted_at=deleted_at)
    
    # Ejecutar la consulta y obtener los resultados
    examenes = query.all()
    
    # Convertir los resultados a JSON
    examenes_json = [
        {
            'id': examen.id, 
            'nombre_examen': examen.nombre_examen, 
            'grado_id': examen.grado_id, 
            'materia_id': examen.materia_id, 
            'especialidad_id': examen.especialidad_id,
            'seccion_id': examen.seccion_id,
            'cantidad_preguntas': examen.cantidad_preguntas,
            'fecha_publicacion': examen.fecha_publicacion,
            'fecha_entrega': examen.fecha_entrega,
            'estado': examen.estado,
            'aproved': examen.aproved,
            'comentario': examen.comentario,
            'created_at': examen.created_at, 
            'updated_at': examen.updated_at, 
            'deleted_at': examen.deleted_at
        }
        for examen in examenes
    ]
    
    return jsonify(examenes_json)


@examen_bp.route('/Eduquest/examenesActualizarEstado/<int:id>', methods=['PUT'])
def actualizar_estado_examen(id):
    try:
        data = request.get_json()
        nuevo_estado = data.get('estado')

        # Obtener el examen por ID
        examen = Examenes.query.get_or_404(id)
        
        # Verificar si el estado está cambiando de False a True
        if not examen.estado and nuevo_estado:
            # Actualizar el estado del examen
            examen.estado = nuevo_estado
            
            # Obtener todos los alumnos que coinciden con especialidad_id, grado_id y seccion_id del examen
            alumnos = Alumnos.query.filter_by(
                especialidad_id=examen.especialidad_id,
                grado_id=examen.grado_id,
                seccion_id=examen.seccion_id
            ).all()
            
            # Crear registros en la tabla examenes_realizados para cada alumno
            for alumno in alumnos:
                examen_realizado = ExamenesResueltos(
                    alumno_id=alumno.id,
                    examen_id=examen.id,
                    puntaje_obtenido=0,
                    completado=False,  # Marcar como no respondido
                    fecha_entregado=None  # Inicialmente sin fecha de entrega
                )
                db.session.add(examen_realizado)
            
            # Confirmar todas las transacciones
            db.session.commit()

        return jsonify({
            'message': 'Estado del examen actualizado y asignado a los alumnos correspondientes' if nuevo_estado else 'Estado del examen actualizado',
            'examen_id': examen.id,
            'estado': examen.estado
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500





@examen_bp.route('/Eduquest/examenesCrear', methods=['POST'])
def crear_examen():
    try:
        # Extraer los datos JSON de la solicitud
        data = request.get_json()

        # Convertir datos al tipo correcto
        estado = data.get('estado')
        if isinstance(estado, str):
            estado = estado.lower() in ['true', '1']

        aproved = data.get('aproved')
        if isinstance(aproved, str):
            aproved = aproved.lower() in ['true', '1']

        fecha_publicacion = data.get('fecha_publicacion')
        if fecha_publicacion:
            fecha_publicacion = datetime.strptime(fecha_publicacion, '%Y-%m-%d').date()
        
        fecha_entrega = data.get('fecha_entrega')
        if fecha_entrega:
            fecha_entrega = datetime.strptime(fecha_entrega, '%Y-%m-%d').date()

        # Crear un nuevo objeto Examenes con los datos proporcionados
        nuevo_examen = Examenes(
            nombre_examen=data['nombre_examen'], 
            grado_id=data['grado_id'], 
            materia_id=data['materia_id'],
            especialidad_id=data['especialidad_id'],
            seccion_id=data['seccion_id'], 
            puntaje_total=data['puntaje_total'],
            cantidad_preguntas=data['cantidad_preguntas'],
            fecha_publicacion=fecha_publicacion, 
            fecha_entrega=fecha_entrega, 
            estado=estado,
            aproved=aproved,
            comentario=data['comentario'],
            created_at=datetime.now(), 
            updated_at=datetime.now(), 
            deleted_at=None
        )
        
        # Añadir el nuevo examen a la sesión de la base de datos
        db.session.add(nuevo_examen)
        
        # Confirmar los cambios
        db.session.commit()

        # Devolver una respuesta exitosa con los datos del nuevo examen
        return jsonify({
            'id': nuevo_examen.id, 
            'nombre_examen': nuevo_examen.nombre_examen, 
            'grado_id': nuevo_examen.grado_id, 
            'materia_id': nuevo_examen.materia_id, 
            'especialidad_id': nuevo_examen.especialidad_id,
            'seccion_id': nuevo_examen.seccion_id,  
            'cantidad_preguntas': nuevo_examen.cantidad_preguntas,
            'puntaje_total': nuevo_examen.puntaje_total,
            'fecha_publicacion': nuevo_examen.fecha_publicacion.strftime('%Y-%m-%d') if nuevo_examen.fecha_publicacion else None,
            'fecha_entrega': nuevo_examen.fecha_entrega.strftime('%Y-%m-%d') if nuevo_examen.fecha_entrega else None,
            'estado': nuevo_examen.estado,
            'aproved': nuevo_examen.aproved,
            'comentario': nuevo_examen.comentario,
            'created_at': nuevo_examen.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
            'updated_at': nuevo_examen.updated_at.strftime('%Y-%m-%d %H:%M:%S'), 
            'deleted_at': nuevo_examen.deleted_at
        }), 201
    except Exception as e:
        # Deshacer cambios en caso de error
        db.session.rollback()
        # Devolver una respuesta de error
        return jsonify({'error': str(e)}), 500



import logging

@examen_bp.route('/Eduquest/examenesActualizar/<int:id>', methods=['PUT'])
def actualizar_examen(id):
    try:
        data = request.get_json()

        examen = Examenes.query.get_or_404(id)

        estado = data.get('estado')
        if estado is not None:
            if isinstance(estado, str):
                estado = estado.lower() in ['true', '1']
            examen.estado = estado

        aproved = data.get('aproved')
        if aproved is not None:
            if isinstance(aproved, str):
                aproved = aproved.lower() in ['true', '1']
            examen.aproved = aproved

        fecha_publicacion = data.get('fecha_publicacion')
        if fecha_publicacion:
            fecha_publicacion = datetime.strptime(fecha_publicacion, '%Y-%m-%d').date()
            examen.fecha_publicacion = fecha_publicacion

        fecha_entrega = data.get('fecha_entrega')
        if fecha_entrega:
            fecha_entrega = datetime.strptime(fecha_entrega, '%Y-%m-%d').date()
            examen.fecha_entrega = fecha_entrega

        examen.nombre_examen = data.get('nombre_examen', examen.nombre_examen)
        examen.grado_id = data.get('grado_id', examen.grado_id)
        examen.materia_id = data.get('materia_id', examen.materia_id)
        examen.especialidad_id = data.get('especialidad_id', examen.especialidad_id)
        examen.seccion_id = data.get('seccion_id', examen.seccion_id)
        examen.cantidad_preguntas = data.get('cantidad_preguntas', examen.cantidad_preguntas)
        examen.comentario = data.get('comentario', examen.comentario)
        examen.created_at = data.get('created_at', examen.created_at)
        examen.updated_at = data.get('updated_at', datetime.now())
        examen.deleted_at = data.get('deleted_at', examen.deleted_at)

        db.session.commit()

        return jsonify({
            'id': examen.id,
            'nombre_examen': examen.nombre_examen,
            'grado_id': examen.grado_id,
            'materia_id': examen.materia_id,
            'especialidad_id': examen.especialidad_id,
            'seccion_id': examen.seccion_id,
            'cantidad_preguntas': examen.cantidad_preguntas,
            'fecha_publicacion': examen.fecha_publicacion,
            'fecha_entrega': examen.fecha_entrega,
            'estado': examen.estado,
            'aproved': examen.aproved,
            'comentario': examen.comentario,
            'created_at': examen.created_at,
            'updated_at': examen.updated_at,
            'deleted_at': examen.deleted_at
        })
    except Exception as e:
        db.session.rollback()
        # Log the error for debugging
        logging.error(f"Error updating exam: {e}", exc_info=True)
        return jsonify({'error': 'Internal Server Error'}), 500
    

@examen_bp.route('/Eduquest/EliminarExamen/<int:id>', methods=['DELETE'])
def eliminar_examen(id):
    # Obtener el examen a eliminar
    examen = Examenes.query.get_or_404(id)

    try:
        # Iniciar una transacción para manejar la eliminación
        with db.session.no_autoflush:
            # Eliminar exámenes resueltos relacionados
            examenes_resueltos_relacionados = ExamenesResueltos.query.filter_by(examen_id=id).all()
            print(f'Exámenes resueltos relacionados encontrados: {len(examenes_resueltos_relacionados)}')
            for examen_resuelto in examenes_resueltos_relacionados:
                db.session.delete(examen_resuelto)
            
            # Confirmar la transacción para eliminar exámenes resueltos
            db.session.commit()

            # Eliminar preguntas respondidas relacionadas
            preguntas_respondidas_relacionadas = PreguntaRespondida.query.join(Preguntas).filter(Preguntas.examen_id == id).all()
            print(f'Preguntas respondidas relacionadas encontradas: {len(preguntas_respondidas_relacionadas)}')
            for pregunta_respondida in preguntas_respondidas_relacionadas:
                db.session.delete(pregunta_respondida)
            
            # Confirmar la transacción para eliminar preguntas respondidas
            db.session.commit()

            # Eliminar respuestas relacionadas
            respuestas_relacionadas = Respuestas.query.join(Preguntas).filter(Preguntas.examen_id == id).all()
            print(f'Respuestas relacionadas encontradas: {len(respuestas_relacionadas)}')
            for respuesta in respuestas_relacionadas:
                db.session.delete(respuesta)
            
            # Confirmar la transacción para eliminar respuestas
            db.session.commit()

            # Eliminar preguntas relacionadas
            preguntas_relacionadas = Preguntas.query.filter_by(examen_id=id).all()
            print(f'Preguntas relacionadas encontradas: {len(preguntas_relacionadas)}')
            for pregunta in preguntas_relacionadas:
                db.session.delete(pregunta)
            
            # Confirmar la transacción para eliminar preguntas
            db.session.commit()

            # Eliminar el examen
            db.session.delete(examen)

        # Confirmar la transacción final para eliminar el examen
        db.session.commit()
        
        return jsonify({'message': 'Examen y sus relaciones eliminados exitosamente.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar el examen.', 'error': str(e)}), 500

    
@examen_bp.route('/Eduquest/examenesBuscarPorID_2/<int:id>', methods=['GET'])
def buscar_examenes_por_id_2(id):
    # Recuperar el examen
    examen = db.session.query(
        Examenes,
        Grados.nombre.label('nombre_grado'),
        Especialidades.nombre.label('nombre_especialidad'),
        Materias.nombre.label('nombre_materia'),
        Secciones.nombre.label('nombre_seccion')
    ).join(Grados, Examenes.grado_id == Grados.id)\
    .join(Especialidades, Examenes.especialidad_id == Especialidades.id)\
    .join(Materias, Examenes.materia_id == Materias.id)\
    .join(Secciones, Examenes.seccion_id == Secciones.id)\
    .filter(Examenes.id == id).first_or_404()

    # Recuperar las preguntas del examen
    preguntas = Preguntas.query.filter_by(examen_id=id).all()
    
    examen_con_preguntas_y_respuestas = {
        'id': examen.Examenes.id, 
        'nombre_examen': examen.Examenes.nombre_examen, 
        'grado_id': examen.Examenes.grado_id, 
        'nombre_grado': examen.nombre_grado,
        'materia_id': examen.Examenes.materia_id, 
        'nombre_materia': examen.nombre_materia,
        'especialidad_id': examen.Examenes.especialidad_id,
        'nombre_especialidad': examen.nombre_especialidad,
        'seccion_id': examen.Examenes.seccion_id,
        'nombre_seccion': examen.nombre_seccion,
        'puntaje_total': examen.Examenes.puntaje_total,
        'cantidad_preguntas': examen.Examenes.cantidad_preguntas,
        'fecha_publicacion': examen.Examenes.fecha_publicacion,
        'fecha_entrega': examen.Examenes.fecha_entrega,
        'estado': examen.Examenes.estado,
        'aproved': examen.Examenes.aproved,
        'comentario': examen.Examenes.comentario,
        'preguntas': []
    }

    for pregunta in preguntas:
        respuestas = Respuestas.query.filter_by(pregunta_id=pregunta.id).all()
        pregunta_con_respuestas = {
            'id': pregunta.id,
            'pregunta': pregunta.pregunta,
            'respuestas': [{
                'id': respuesta.id,
                'pregunta_id': respuesta.pregunta_id,
                'respuesta': respuesta.respuesta,
                'es_correcta': respuesta.es_correcta
            } for respuesta in respuestas]
        }
        examen_con_preguntas_y_respuestas['preguntas'].append(pregunta_con_respuestas)

    return jsonify(examen_con_preguntas_y_respuestas)




@examen_bp.route('/Eduquest/examenesBuscarPorID_3/<int:examen_id>/<int:alumno_id>', methods=['GET'])
def buscar_examenes_por_id_3(examen_id, alumno_id):
    # Recuperar el examen
    examen = db.session.query(
        Examenes,
        Grados.nombre.label('nombre_grado'),
        Especialidades.nombre.label('nombre_especialidad'),
        Materias.nombre.label('nombre_materia'),
        Secciones.nombre.label('nombre_seccion')
    ).join(Grados, Examenes.grado_id == Grados.id)\
    .join(Especialidades, Examenes.especialidad_id == Especialidades.id)\
    .join(Materias, Examenes.materia_id == Materias.id)\
    .join(Secciones, Examenes.seccion_id == Secciones.id)\
    .filter(Examenes.id == examen_id).first_or_404()

    # Recuperar las preguntas del examen
    preguntas = Preguntas.query.filter_by(examen_id=examen_id).all()
    
    # Recuperar las respuestas del alumno para este examen
    respuestas_respondidas = PreguntaRespondida.query.filter_by(examen_id=examen_id, alumno_id=alumno_id).all()
    
    # Crear un diccionario para almacenar las respuestas del alumno
    respuestas_por_pregunta = {respuesta.pregunta_id: respuesta for respuesta in respuestas_respondidas}
    
    # Recuperar el puntaje obtenido por el alumno en este examen
    examen_resuelto = ExamenesResueltos.query.filter_by(examen_id=examen_id, alumno_id=alumno_id).first()
    if not examen_resuelto:
        return jsonify({"message": "Examen resuelto no encontrado"}), 404
    puntaje_obtenido = examen_resuelto.puntaje_obtenido
    print(f'Puntaje obtenido recuperado: {puntaje_obtenido}')

    examen_con_preguntas_y_respuestas = {
        'id': examen.Examenes.id,
        'nombre_examen': examen.Examenes.nombre_examen,
        'grado_id': examen.Examenes.grado_id,
        'nombre_grado': examen.nombre_grado,
        'materia_id': examen.Examenes.materia_id,
        'nombre_materia': examen.nombre_materia,
        'especialidad_id': examen.Examenes.especialidad_id,
        'nombre_especialidad': examen.nombre_especialidad,
        'seccion_id': examen.Examenes.seccion_id,
        'nombre_seccion': examen.nombre_seccion,
        'puntaje_total': examen.Examenes.puntaje_total,
        'cantidad_preguntas': examen.Examenes.cantidad_preguntas,
        'fecha_publicacion': examen.Examenes.fecha_publicacion,
        'fecha_entrega': examen.Examenes.fecha_entrega,
        'estado': examen.Examenes.estado,
        'aproved': examen.Examenes.aproved,
        'comentario': examen.Examenes.comentario,
        'puntaje_obtenido': puntaje_obtenido,
        'preguntas': []
    }

    for pregunta in preguntas:
        respuestas = Respuestas.query.filter_by(pregunta_id=pregunta.id).all()
        respuesta_alumno = respuestas_por_pregunta.get(pregunta.id)
        respuesta_elegida = None
        if respuesta_alumno:
            respuesta_elegida = Respuestas.query.get(respuesta_alumno.respuesta_id)

        pregunta_con_respuestas = {
            'id': pregunta.id,
            'pregunta': pregunta.pregunta,
            'respuestas': [{
                'id': respuesta.id,
                'pregunta_id': respuesta.pregunta_id,
                'respuesta': respuesta.respuesta,
                'es_correcta': respuesta.es_correcta
            } for respuesta in respuestas],
            'respuesta_alumno': respuesta_alumno.respuesta_id if respuesta_alumno else None,
            'respuesta_alumno_texto': respuesta_elegida.respuesta if respuesta_elegida else None,
            'puntos_obtenidos': float(respuesta_alumno.puntos_obtenidos) if respuesta_alumno else 0.0
        }
        examen_con_preguntas_y_respuestas['preguntas'].append(pregunta_con_respuestas)

    return jsonify(examen_con_preguntas_y_respuestas)
