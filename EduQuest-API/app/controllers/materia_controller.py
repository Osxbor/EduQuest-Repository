from flask import Blueprint, request, jsonify
from ..models.materias import Materias
from .. import db
from datetime import datetime

materia_bp = Blueprint('materia_bp', __name__)

#@app.route() es un DECORADOR que define la ruta en la que se puede encontrar la función, en este caso, buscar_materias().
#methods es un PARAMETRO para definir qué método HTTP puede usar la ruta que se especifíca en el DECORADOR
@materia_bp.route('/Eduquest/materiasBuscar', methods=['GET'])
def buscar_materias():
    
    #Se utiliza el modelo Materias
    #all() está recuperando todos los registros de la tabla que está asociada al modelo Materias
    #materias va a ser una lista de objetos, estos objetos representarán un registro en la tabla materias
    materias = Materias.query.all()

    #'for g in materias' es un BUCLE DE LA COMPRESIÓN DE LISTA. 'lista' es una lista que contiene los registros de la base de datos,
    # esta compresión de lista itera sobre cada objeto g. Para cada objeto crea un diccionario que mapea los atributos a sus respectivos valores de 'g'.
    # en la lista, cada elemento 'g' es un OBJETO que represnta una sola materia.
    #josonify() convierte el objeto Pyhton (lo que está dentro de sus paréntesis, es decir, 
    # la lista de dicciionarios) en una respuesta .JSON
    return jsonify([{
        'id': g.id, 
        'nombre': g.nombre, 
        'created_at': g.created_at, 
        'updated_at': g.updated_at, 
        'deleted_at': g.deleted_at
        } for g in materias])

@materia_bp.route('/Eduquest/materiasCrear', methods=['POST'])
def crear_materia():
    try:
        #'request.get_json()' es una FUNCIÓN de FLASK, la cual se encarga de extraer los datos en formato JSON del cuerpo de solicitud entrante
        data = request.get_json()
        
        #Se crea un objeto nuevo (nuevo_grado) del modelo Materias 
        # 'data' es un DICCIONARIO contiene los valores enviados en la solicitud POST, estos datos crean el objeto 'nuevo_materia'
        nuevo_materia = Materias(
            nombre=data['nombre'], 
            created_at=datetime.now(), 
            updated_at=datetime.now(), 
            deleted_at=None
        )
        
        #'db.session' se refiere a una "sesión", la cual es el área de trabajo donde se realizan todas las operaciones de la base de datos-
        # -antes de que se guarden o eliminen permanentemente. 
        #En resumen, una "sesión" es donde se preparan todas las transacciones antes de realmente modificar la base de datos.
    
        #'db.session.add()' añade el objeto 'nuevo_materia' a la sesión de base de datos, lo que prepara al objeto para ser-
        # -guardado en la base de datos.
        db.session.add(nuevo_materia)
        
        #'db.session.commit()' ejecuta el comando SQL para guardar los cambios en la base de datos. El grado nuevo es insertado en la tabla que le corresponde.
        db.session.commit()
        
        #Si no hay ningún error durante la TRANSACCIÓN entonces retornará los valores ingresados en el formato JSON.
        #jsonify() Convierte el diccionario que contiene los atributos del 'nuevo_materia' a una respuesta JSON.
        #201 es uno de los códigos de estado HTTP que se envian junto con la respuesta JSON. Este código indica que la solicitud ha creado un recurso (en este caso en la base de datos).
        return jsonify({'id': nuevo_materia.id, 'nombre': nuevo_materia.nombre, 'created_at': nuevo_materia.created_at, 'updated_at': nuevo_materia.updated_at, 'deleted_at': nuevo_materia.deleted_at}), 201
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.


@materia_bp.route('/Eduquest/materiasActualizar/<int:id>', methods=['PUT'])
def actualizar_materia(id):
    try:
        #'request.get_json()' va a extraer los datos enviados en la solicitud, a este punto se espera que ya estén en formato JSON-
        #request.get_json() convierte el cuerpo de la solicitud JSON en un DICCIONARIO de Python, al que luego se accede con el nombre 'data'.
        #-Estos datos serán usados para actualizar el registro existente.
        data = request.get_json()

        materia = Materias.query.get_or_404(id)
        materia.nombre = data.get('nombre', materia.nombre)
        materia.created_at = data.get('created_at', materia.created_at)
        materia.updated_at = data.get('updated_at', datetime.now()) #datetime.now() es, en esta línea de código, para establecer la hora y fecha en la que fue modificado el registro
        materia.deleted_at = data.get('deleted_at', materia.deleted_at)
        
        #'db.session.commit()' ejecuta el comando SQL para guardar los cambios en la base de datos. La materia nuevo es insertado en la tabla que le corresponde.
        db.session.commit()

        #Aquí devuelve una respuesta en formato JSON, con los ATRIBUTOS del OBJETO 'grado' actualizados.
        return jsonify({
            'id': materia.id, 
            'nombre': materia.nombre, 
            'created_at': materia.created_at, 
            'updated_at': materia.updated_at, 
            'deleted_at': materia.deleted_at})
    
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.


@materia_bp.route('/Eduquest/materiasEliminar/<int:id>', methods=['DELETE'])
def eliminar_materia(id):
    try:
        #Aquí va a buscar el registro en la base de datos, usando como parámetro el id.
        #El METODO get_or_404() básicamente intentará OBTENER el registro existente en la Base de datos Ó devolverá una respuesta 404 (recurso no encontrado).
        materia = Materias.query.get_or_404(id)
        
        # db.session.delete(materia) es una LLAMADA a una FUNCIÓN de SQLAlchemy
        #Una vez encontrado el registro,'db.session.delete(materia)' lo marca para ser eliminado de la base de datos.
        #OJO: no lo elimina, solo prepara la "transacción" para ser confirmada la eliminación
        # 'delete(materia)' es un método de la "sesión".
        db.session.delete(materia)
        
        #'db.session.commit()' Finaliza la "transacción" ejecuta el comando SQL para ELIMINAR el registro en la base de datos.
        db.session.commit()
        return jsonify({'message': f'Materia {id} fue eliminado con éxito'})
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.