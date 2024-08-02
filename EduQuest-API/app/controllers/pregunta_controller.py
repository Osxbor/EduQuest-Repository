from flask import Blueprint, request, jsonify
from ..models.preguntas import Preguntas
from .. import db
from datetime import datetime

pregunta_bp = Blueprint('pregunta_bp', __name__)

#@app.route() es un DECORADOR que define la ruta en la que se puede encontrar la función, en este caso, buscar_preguntas().
#methods es un PARAMETRO para definir qué método HTTP puede usar la ruta que se especifíca en el DECORADOR
@pregunta_bp.route('/Eduquest/preguntasBuscar', methods=['GET'])
def buscar_preguntas():

    #Se utiliza el modelo Preguntas
    #all() está recuperando todos los registros de la tabla que está asociada al modelo Preguntas
    #preguntas va a ser una lista de objetos, estos objetos representarán un registro en la tabla preguntas
    preguntas = Preguntas.query.all()

    #'for g in preguntas' es un BUCLE DE LA COMPRESIÓN DE LISTA. 'lista' es una lista que contiene los registros de la base de datos,
    # esta compresión de lista itera sobre cada objeto g. Para cada objeto crea un diccionario que mapea los atributos a sus respectivos valores de 'g'.
    # en la lista, cada elemento 'g' es un OBJETO que represnta una sola pregunta.
    #josonify() convierte el objeto Pyhton (lo que está dentro de sus paréntesis, es decir, 
    # la lista de dicciionarios) en una respuesta .JSON
    return jsonify([{
        'id': g.id, 
        'examen_id':g.examen_id, 
        'pregunta': g.pregunta, 
        'created_at': g.created_at, 
        'updated_at': g.updated_at, 
        'deleted_at': g.deleted_at
        } for g in preguntas])


@pregunta_bp.route('/Eduquest/preguntasBuscarPorId/<int:id>', methods=['GET'])
def buscar_preguntas_por_id(id):
    pregunta = Preguntas.query.get_or_404(id)
    return jsonify({
        'id': pregunta.id, 
        'examen_id': pregunta.examen_id, 
        'pregunta': pregunta.pregunta, 
        'created_at': pregunta.created_at, 
        'updated_at': pregunta.updated_at, 
        'deleted_at': pregunta.deleted_at
    })

@pregunta_bp.route('/Eduquest/preguntasBuscarPorExamenId/<int:examen_id>', methods=['GET'])
def buscar_preguntas_por_examen_id(examen_id):
    preguntas = Preguntas.query.filter_by(examen_id=examen_id).all()
    if not preguntas:
        return jsonify({'message': 'No se encontraron preguntas para este examen_id.'}), 404

    preguntas_list = [{
        'id': pregunta.id, 
        'examen_id': pregunta.examen_id, 
        'pregunta': pregunta.pregunta, 
        'created_at': pregunta.created_at, 
        'updated_at': pregunta.updated_at, 
        'deleted_at': pregunta.deleted_at
    } for pregunta in preguntas]

    return jsonify(preguntas_list)


@pregunta_bp.route('/Eduquest/preguntasCrear', methods=['POST'])
def crear_pregunta():
    try:
        #'request.get_json()' es una FUNCIÓN de FLASK, la cual se encarga de extraer los datos en formato JSON del cuerpo de solicitud entrante 
        data = request.get_json()

        #Se crea un objeto nuevo (nuevo_grado) del modelo Preguntas 
        # 'data' es un DICCIONARIO contiene los valores enviados en la solicitud POST, estos datos crean el objeto 'nueva_pregunta'
        nueva_pregunta = Preguntas(
            examen_id=data['examen_id'], 
            pregunta=data['pregunta'], 
            created_at=datetime.now(), 
            updated_at=datetime.now(), 
            deleted_at=None
            )
        
        #'db.session' se refiere a una "sesión", la cual es el área de trabajo donde se realizan todas las operaciones de la base de datos-
        # -antes de que se guarden o eliminen permanentemente. 
        #En resumen, una "sesión" es donde se preparan todas las transacciones antes de realmente modificar la base de datos.
    
        #'db.session.add()' añade el objeto 'nuevo_grado' a la sesión de base de datos, lo que prepara al objeto para ser-
        # -guardado en la base de datos.
        db.session.add(nueva_pregunta)
        
        #'db.session.commit()' ejecuta el comando SQL para guardar los cambios en la base de datos. El grado nuevo es insertado en la tabla que le corresponde.
        db.session.commit()
        
        #Si no hay ningún error durante la TRANSACCIÓN entonces retornará los valores ingresados en el formato JSON.
        #jsonify() Convierte el diccionario que contiene los atributos del 'nueva_pregunta' a una respuesta JSON.
        #201 es uno de los códigos de estado HTTP que se envian junto con la respuesta JSON. Este código indica que la solicitud ha creado un recurso (en este caso en la base de datos).
        return jsonify({
            'id': nueva_pregunta.id, 
            'examen_id':nueva_pregunta.examen_id ,
            'pregunta': nueva_pregunta.pregunta, 
            'created_at': nueva_pregunta.created_at, 
            'updated_at': nueva_pregunta.updated_at, 
            'deleted_at': nueva_pregunta.deleted_at}), 201
    
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.


@pregunta_bp.route('/Eduquest/preguntasActualizar/<int:id>', methods=['PUT'])
def actualizar_pregunta(id):
    try:
        #'request.get_json()' va a extraer los datos enviados en la solicitud, a este punto se espera que ya estén en formato JSON-
        #request.get_json() convierte el cuerpo de la solicitud JSON en un DICCIONARIO de Python, al que luego se accede con el nombre 'data'.
        #-Estos datos serán usados para actualizar el registro existente.
        data = request.get_json()

        #Aquí va a buscar el registro en la base de datos, usando como parámetro el id.
        #El METODO get_or_404() básicamente intentará OBTENER el registro existente en la Base de datos O devolverá una respuesta 404 (recurso no encontrado).
        pregunta = Preguntas.query.get_or_404(id)
        pregunta.examen_id = data.get('examen_id', pregunta.examen_id)
        pregunta.pregunta = data.get('pregunta', pregunta.pregunta)


        if 'created_at' in data and data['created_at']:
            pregunta.created_at = data['created_at']
        if 'updated_at' in data and data['updated_at']:
            pregunta.updated_at = datetime.now()  # Actualiza con la fecha y hora actual
        if 'deleted_at' in data:
            pregunta.deleted_at = data['deleted_at']
        
        #'db.session.commit()' ejecuta el comando SQL para guardar los cambios en la base de datos. La nueva pregunta es insertado en la tabla que le corresponde.
        db.session.commit()

        #Aquí devuelve una respuesta en formato JSON, con los ATRIBUTOS del OBJETO 'grado' actualizados.
        return jsonify({
            'id': pregunta.id,
            'examen_id': pregunta.examen_id,
            'pregunta': pregunta.pregunta,
            'created_at': pregunta.created_at,
            'updated_at': pregunta.updated_at,
            'deleted_at': pregunta.deleted_at
        })
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.

    

@pregunta_bp.route('/Eduquest/preguntasEliminar/<int:id>', methods=['DELETE'])
def eliminar_pregunta(id):
    try:

        #Aquí va a buscar el registro en la base de datos, usando como parámetro el id.
        #El METODO get_or_404() básicamente intentará OBTENER el registro existente en la Base de datos Ó devolverá una respuesta 404 (recurso no encontrado).
        pregunta = Preguntas.query.get_or_404(id)
        
        # db.session.delete(pregunta) es una LLAMADA a una FUNCIÓN de SQLAlchemy
        #Una vez encontrado el registro,'db.session.delete(pregunta)' lo marca para ser eliminado de la base de datos.
        #OJO: no lo elimina, solo prepara la "transacción" para ser confirmada la eliminación
        # 'delete(pregunta)' es un método de la "sesión".
        db.session.delete(pregunta)
        
        #'db.session.commit()' Finaliza la "transacción" ejecuta el comando SQL para ELIMINAR el registro en la base de datos.
        db.session.commit()
        return jsonify({'message': f'Pregunta {id} fue eliminado con éxito'})
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.