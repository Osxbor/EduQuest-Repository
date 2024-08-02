from flask import Blueprint, request, jsonify
from .. import db
from ..models.examenes import Examenes
from ..models.preguntas_respondidas import PreguntaRespondida
from ..models.examenes_resueltos import ExamenesResueltos
from ..models.respuestas import Respuestas
from datetime import datetime

responder_bp = Blueprint('responder_bp', __name__)


@responder_bp.route('/Eduquest/guardarRespuestas', methods=['POST'])
def guardar_respuestas():
    data = request.get_json()
    print('Datos recibidos:', data)
    
    examen_id = data.get('examen_id')
    alumno_id = data.get('alumno_id')
    respuestas = data.get('respuestas')

    if not examen_id or not alumno_id or not respuestas:
        return jsonify({"message": "Faltan datos"}), 400

    try:
        # Obtener el examen para calcular el puntaje total
        examen = Examenes.query.filter_by(id=examen_id).first()
        if not examen:
            return jsonify({"message": "Examen no encontrado"}), 404
        
        puntaje_total = examen.puntaje_total
        cantidad_preguntas = examen.cantidad_preguntas
        print(f'Examen encontrado: puntaje_total={puntaje_total}, cantidad_preguntas={cantidad_preguntas}')

        # Variables para calcular puntaje obtenido
        correctas = 0

        for respuesta in respuestas:
            print('Procesando respuesta:', respuesta)
            pregunta_id = respuesta.get('pregunta_id')
            respuesta_id = respuesta.get('respuesta_id')
            
            # Obtener si la respuesta es correcta desde la base de datos
            respuesta_correcta = Respuestas.query.filter_by(id=respuesta_id, pregunta_id=pregunta_id).first()
            if respuesta_correcta:
                es_correcta = respuesta_correcta.es_correcta
                puntos_obtenidos = puntaje_total / cantidad_preguntas if es_correcta else 0
                pregunta_respondida = PreguntaRespondida(
                    examen_id=examen_id,
                    alumno_id=alumno_id,
                    pregunta_id=pregunta_id,
                    respuesta_id=respuesta_id,
                    es_correcta=es_correcta,
                    puntos_obtenidos=puntos_obtenidos,
                    respondida=True
                )
                db.session.add(pregunta_respondida)
                if es_correcta:
                    correctas += 1
            else:
                print(f'Respuesta no encontrada para pregunta_id={pregunta_id} y respuesta_id={respuesta_id}')

        # Calcular el puntaje obtenido basado en las respuestas correctas
        puntaje_obtenido = int((correctas / cantidad_preguntas) * puntaje_total)
        print(f'Puntaje obtenido calculado: {puntaje_obtenido}')

        # Buscar si existe un registro previo en ExamenesResueltos
        examen_resuelto = ExamenesResueltos.query.filter_by(examen_id=examen_id, alumno_id=alumno_id).first()

        if examen_resuelto:
            examen_resuelto.puntaje_obtenido = puntaje_obtenido
            examen_resuelto.completado = True
            examen_resuelto.updated_at = datetime.utcnow()
        else:
            # Crear un nuevo registro en ExamenesResueltos si no existe
            examen_resuelto = ExamenesResueltos(
                examen_id=examen_id,
                alumno_id=alumno_id,
                puntaje_obtenido=puntaje_obtenido,
                completado=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(examen_resuelto)

        db.session.commit()
        return jsonify({"message": "Respuestas guardadas correctamente", "puntaje_obtenido": puntaje_obtenido}), 200
    except Exception as e:
        db.session.rollback()
        print(str(e))  # Print the exception for debugging purposes
        return jsonify({"message": str(e)}), 500
