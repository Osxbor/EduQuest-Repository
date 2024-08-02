from flask import Blueprint, request, jsonify
from ..models.respuestas import Respuestas
from .. import db
from datetime import datetime

respuesta_bp = Blueprint('respuesta_bp', __name__)

#@app.route() es un DECORADOR que define la ruta en la que se puede encontrar la función, en este caso, buscar_respuestas().
#methods es un PARAMETRO para definir qué método HTTP puede usar la ruta que se especifíca en el DECORADOR
@respuesta_bp.route('/Eduquest/respuestasBuscar', methods=['GET'])
def buscar_respuestas():

    #Se utiliza el modelo Respuestas
    #all() está recuperando todos los registros de la tabla que está asociada al modelo Respuestas
    #respuestas va a ser una lista de objetos, estos objetos representarán un registro en la tabla respuestas
    respuestas = Respuestas.query.all()

    #'for g in respuestas' es un BUCLE DE LA COMPRESIÓN DE LISTA. 'lista' es una lista que contiene los registros de la base de datos,
    # esta compresión de lista itera sobre cada objeto g. Para cada objeto crea un diccionario que mapea los atributos a sus respectivos valores de 'g'.
    # en la lista, cada elemento 'g' es un OBJETO que represnta una sola respuesta.
    #josonify() convierte el objeto Pyhton (lo que está dentro de sus paréntesis, es decir, 
    # la lista de dicciionarios) en una respuesta .JSON
    return jsonify([{
        'id': g.id,
        'pregunta_id': g.pregunta_id,
        'respuesta': g.respuesta,
        'es_correcta': g.es_correcta,
        'created_at': g.created_at,
        'updated_at': g.updated_at,
        'deleted_at': g.deleted_at
    } for g in respuestas])


@respuesta_bp.route('/Eduquest/respuestasBuscarPorId/<int:id>', methods=['GET'])
def buscar_respuestas_por_id(id):
    respuesta = Respuestas.query.get_or_404(id)
    return jsonify({
        'id': respuesta.id,
        'pregunta_id': respuesta.pregunta_id,
        'respuesta': respuesta.respuesta,
        'es_correcta': respuesta.es_correcta,
        'created_at': respuesta.created_at,
        'updated_at': respuesta.updated_at,
        'deleted_at': respuesta.deleted_at
    })

@respuesta_bp.route('/Eduquest/respuestasBuscarPorPreguntaId/<int:pregunta_id>', methods=['GET'])
def buscar_respuestas_por_pregunta_id(pregunta_id):
    respuestas = Respuestas.query.filter_by(pregunta_id=pregunta_id).all()
    if not respuestas:
        return jsonify({'message': 'No se encontraron respuestas para este pregunta_id.'}), 404

    respuestas_list = [{
        'id': respuesta.id,
        'pregunta_id': respuesta.pregunta_id,
        'respuesta': respuesta.respuesta,
        'es_correcta': respuesta.es_correcta,
        'created_at': respuesta.created_at,
        'updated_at': respuesta.updated_at,
        'deleted_at': respuesta.deleted_at
    } for respuesta in respuestas]

    return jsonify(respuestas_list)


@respuesta_bp.route('/Eduquest/respuestasCrear', methods=['POST'])
def crear_respuestas():
    
    try:
        #'request.get_json()' es una FUNCIÓN de FLASK, la cual se encarga de extraer los datos en formato JSON del cuerpo de solicitud entrante 
        data = request.get_json()

        #Se crea un objeto nuevo (nuevo_grado) del modelo Respuestas 
        # 'data' es un DICCIONARIO contiene los valores enviados en la solicitud POST, estos datos crean el objeto 'nueva_respuesta'
        nueva_respuesta = Respuestas(
            pregunta_id=data['pregunta_id'],
            respuesta=data['respuesta'],
            es_correcta=bool(int(data['es_correcta'])),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=None
        )
        #'db.session' se refiere a una "sesión", la cual es el área de trabajo donde se realizan todas las operaciones de la base de datos-
        # -antes de que se guarden o eliminen permanentemente. 
        #En resumen, una "sesión" es donde se preparan todas las transacciones antes de realmente modificar la base de datos.
    
        #'db.session.add()' añade el objeto 'nuevo_grado' a la sesión de base de datos, lo que prepara al objeto para ser-
        # -guardado en la base de datos.
        db.session.add(nueva_respuesta)
        
        #'db.session.commit()' ejecuta el comando SQL para guardar los cambios en la base de datos. El grado nuevo es insertado en la tabla que le corresponde.
        db.session.commit()
        
        #Si no hay ningún error durante la TRANSACCIÓN entonces retornará los valores ingresados en el formato JSON.
        #jsonify() Convierte el diccionario que contiene los atributos del 'nueva_respuesta' a una respuesta JSON.
        #201 es uno de los códigos de estado HTTP que se envian junto con la respuesta JSON. Este código indica que la solicitud ha creado un recurso (en este caso en la base de datos).
        return jsonify({
            'id': nueva_respuesta.id,
            'pregunta_id': nueva_respuesta.pregunta_id,
            'respuesta': nueva_respuesta.respuesta,
            'es_correcta': nueva_respuesta.es_correcta,
            'created_at': nueva_respuesta.created_at,
            'updated_at': nueva_respuesta.updated_at,
            'deleted_at': nueva_respuesta.deleted_at
        }), 201
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.


@respuesta_bp.route('/Eduquest/respuestasActualizar/<int:id>', methods=['PUT'])
def actualizar_respuestas(id):
    try:
        #'request.get_json()' va a extraer los datos enviados en la solicitud, a este punto se espera que ya estén en formato JSON-
        #request.get_json() convierte el cuerpo de la solicitud JSON en un DICCIONARIO de Python, al que luego se accede con el nombre 'data'.
        #-Estos datos serán usados para actualizar el registro existente.
        data = request.get_json()

        #Aquí va a buscar el registro en la base de datos, usando como parámetro el id.
        #El METODO get_or_404() básicamente intentará OBTENER el registro existente en la Base de datos O devolverá una respuesta 404 (recurso no encontrado).
        respuesta = Respuestas.query.get_or_404(id)

        #CONDICIONES EN LOS CAMPOS PARA PODER ACTUALIZAR:
        #actualiza 'pregunta_id' en el objeto 'respuesta' si 'pregunta_id' está en los datos y no está vacío
        if 'pregunta_id' in data and data['pregunta_id']:
            respuesta.pregunta_id = data['pregunta_id']
        
        #actualiza 'respuesta' en el objeto 'respuesta' si 'respuesta' está en los datos y no está vacío
        if 'respuesta' in data and data['respuesta']:
            respuesta.respuesta = data['respuesta']
        
        #Si 'es_correcta' está en los datos, actualiza 'es_correcta' en el objeto 'respuesta' a la 
        # vez que lo convierte en booleano(True or False).
        if 'es_correcta' in data:
            respuesta.es_correcta = bool(int(data['es_correcta']))
        
        # Actualiza el campo con la fecha y hora actuales.
        respuesta.updated_at = datetime.now()
        
        #Si el campo 'deleted_at' está en los datos, actualiza 'deleted_at' en el 
        # objeto 'respuesta', permitiendo establecerlo en 'None'.
        if 'deleted_at' in data:
            respuesta.deleted_at = data['deleted_at'] if data['deleted_at'] else None
        
        #'db.session.commit()' ejecuta el comando SQL para guardar los cambios en la base de datos. La respuesta nueva es insertado en la tabla que le corresponde.
        db.session.commit()

        #Aquí devuelve una respuesta en formato JSON, con los ATRIBUTOS del OBJETO 'grado' actualizados.
        return jsonify({
            'id': respuesta.id,
            'pregunta_id': respuesta.pregunta_id,
            'respuesta': respuesta.respuesta,
            'es_correcta': respuesta.es_correcta,
            'created_at': respuesta.created_at,
            'updated_at': respuesta.updated_at,
            'deleted_at': respuesta.deleted_at
        })
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.


@respuesta_bp.route('/Eduquest/respuestasEliminar/<int:id>', methods=['DELETE'])
def eliminar_respuestas(id):
    try:
        #Aquí va a buscar el registro en la base de datos, usando como parámetro el id.
        #El METODO get_or_404() básicamente intentará OBTENER el registro existente en la Base de datos Ó devolverá una respuesta 404 (recurso no encontrado).
        respuesta = Respuestas.query.get_or_404(id)
        
        # db.session.delete(respuesta) es una LLAMADA a una FUNCIÓN de SQLAlchemy
        #Una vez encontrado el registro,'db.session.delete(respuesta)' lo marca para ser eliminado de la base de datos.
        #OJO: no lo elimina, solo prepara la "transacción" para ser confirmada la eliminación
        # 'delete(respuesta)' es un método de la "sesión".
        db.session.delete(respuesta)
        
        #'db.session.commit()' Finaliza la "transacción" ejecuta el comando SQL para ELIMINAR el registro en la base de datos.
        db.session.commit()
        return jsonify({'message': f'Respuesta {id} fue eliminada con éxito'})
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.