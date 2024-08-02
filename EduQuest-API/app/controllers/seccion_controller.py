from flask import Blueprint, request, jsonify
from ..models.secciones import Secciones
from .. import db
from datetime import datetime

seccion_bp = Blueprint('seccion_bp', __name__)

#@app.route() es un DECORADOR que define la ruta en la que se puede encontrar la función, en este caso, obtener_seccion().
#methods es un PARAMETRO para definir qué método HTTP puede usar la ruta que se especifíca en el DECORADOR
@seccion_bp.route('/Eduquest/seccionBuscar', methods=['GET'])
def obtener_seccion():#Se define la función obtener_seccion()

    #Se utiliza el modelo Secciones
    #all() está recuperando todos los registros de la tabla que está asociada al modelo Grado
    #grados va a ser una lista de objetos, estos objetos representarán un registro en la tabla grados
    seccion = Secciones.query.all()

    #'for g in seccion' es un BUCLE DE LA COMPRESIÓN DE LISTA. 'lista' es una lista que contiene los registros de la base de datos,
    # esta compresión de lista itera sobre cada objeto g. Para cada objeto crea un diccionario que mapea los atributos a sus respectivos valores de 'g'.
    # en la lista, cada elemento 'g' es un OBJETO que represnta un solo seccion.
    #josonify() convierte el objeto Pyhton (lo que está dentro de sus paréntesis, es decir, 
    # la lista de diccionarios) en una respuesta .JSON
    return jsonify([{
        'id': g.id, 
        'nombre': g.nombre, 
        'created_at': g.created_at, 
        'updated_at': g.updated_at, 
        'deleted_at': g.deleted_at
        } for g in seccion])

#DECORADOR que indica que la función crear_seccion() manejará las solicitudes HTTP POST (las cuales aceptará únicamente) en la url '/Eduquest/seccionCrear'
# POST envía datos al servidor.
@seccion_bp.route('/Eduquest/seccionCrear', methods=['POST'])
def crear_seccion(): #Esta línea DEFINE la función crear_seccion()
    try:
        #'request.get_json()' es una FUNCIÓN de FLASK, la cual se encarga de extraer los datos en formato JSON del cuerpo de solicitud entrante 
        data = request.get_json()
        #Se crea un objeto nuevo (nueva_seccion) del modelo Secciones 
        # 'data' es un DICCIONARIO contiene los valores enviados en la solicitud POST, estos datos crean el objeto 'nueva_seccion'
        nueva_seccion = Secciones(
            nombre=data['nombre'], 
            created_at=datetime.now(), 
            updated_at=datetime.now(), 
            deleted_at=None
        )

        #'db.session' se refiere a una "sesión", la cual es el área de trabajo donde se realizan todas las operaciones de la base de datos-
        # -antes de que se guarden o eliminen permanentemente. 
        #En resumen, una "sesión" es donde se preparan todas las transacciones antes de realmente modificar la base de datos.
    
        #'db.session.add()' añade el objeto 'nueva_seccion' a la sesión de base de datos, lo que prepara al objeto para ser-
        # -guardado en la base de datos.
        db.session.add(nueva_seccion)

        #'db.session.commit()' ejecuta el comando SQL para guardar los cambios en la base de datos. La seccion nueva es insertado en la tabla que le corresponde.
        db.session.commit()
        
        #Si no hay ningún error durante la TRANSACCIÓN entonces retornará los valores ingresados en el formato JSON.
        #jsonify() Convierte el diccionario que contiene los atributos del 'nueva_seccion' a una respuesta JSON.
        #201 es uno de los códigos de estado HTTP que se envian junto con la respuesta JSON. Este código indica que la solicitud ha creado un recurso (en este caso en la base de datos).
        return jsonify({
            'id': nueva_seccion.id, 
            'nombre': nueva_seccion.nombre, 
            'created_at': nueva_seccion.created_at, 
            'updated_at': nueva_seccion.updated_at, 
            'deleted_at': nueva_seccion.deleted_at
            }), 201
    except Exception as e: #PERO si se provoca una EXCEPCIÓN entonces...
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.



#@app.route es el DECORADOR que asocia la URL '/Eduquest/seccionActualizar/<int:id>' con la FUNCIÓN actualizar_seccion(id), la cual hará solo solicitudes HTTP PUT
@seccion_bp.route('/Eduquest/seccionActualizar/<int:id>', methods=['PUT'])
#Define la FUNCIÓN, donde id es el parámetro para identificar qué registro en la base de datos va a ser actualizardo
def actualizar_seccion(id):
    try:
        #'request.get_json()' va a extraer los datos enviados en la solicitud, a este punto se espera que ya estén en formato JSON-
        #request.get_json() convierte el cuerpo de la solicitud JSON en un DICCIONARIO de Python, al que luego se accede con el nombre 'data'.
        #-Estos datos serán usados para actualizar el registro existente.
        data = request.get_json()
        
        #Aquí va a buscar el registro en la base de datos, usando como parámetro el id.
        #El METODO get_or_404() básicamente intentará OBTENER el registro existente en la Base de datos O devolverá una respuesta 404 (recurso no encontrado).
        seccion = Secciones.query.get_or_404(id)

        #Todo este bloque Actualiza los atributos del OBJETO seccion con los valores que se les dió en la solicitud POST.
        #Si alguno de los valores no se encuentra en data entonces se mantiene con el mismo valor del objeto.
        #'get()' es un método del diccionario 'data'.
        seccion.nombre = data.get('nombre', seccion.nombre)
        seccion.created_at = data.get('created_at', seccion.created_at)
        seccion.updated_at = data.get('updated_at', datetime.now()) #datetime.now() es, en esta línea de código, para establecer la hora y fecha en la que fue modificado el registro
        seccion.deleted_at = data.get('deleted_at', seccion.deleted_at)
        
        #'db.session.commit()' ejecuta el comando SQL para guardar los cambios en la base de datos. La seccion nuevo es insertado en la tabla que le corresponde.
        db.session.commit()
        #Aquí devuelve una respuesta en formato JSON, con los ATRIBUTOS del OBJETO 'seccion' actualizados.
        return jsonify({
            'id': seccion.id, 
            'nombre': seccion.nombre, 
            'created_at': seccion.created_at, 
            'updated_at': seccion.updated_at, 
            'deleted_at': seccion.deleted_at
            })
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.


#@app.route es el DECORADOR que asocia la URL '/Eduquest/especialidadEliminar/<int:id>' con la FUNCIÓN eliminar_especialidad(id), la cual hará solo solicitudes HTTP DELETE
@seccion_bp.route('/Eduquest/seccionEliminar/<int:id>', methods=['DELETE'])
#Define la FUNCIÓN, donde id es el parámetro para identificar qué registro en la base de datos va a ser eliminado.
def eliminar_seccion(id):
    try:
        #Aquí va a buscar el registro en la base de datos, usando como parámetro el id.
        #El METODO get_or_404() básicamente intentará OBTENER el registro existente en la Base de datos O devolverá una respuesta 404 (recurso no encontrado).
        seccion = Secciones.query.get_or_404(id)
        
        # db.session.delete(seccion) es una LLAMADA a una FUNCIÓN de SQLAlchemy
        #Una vez encontrado el registro,'db.session.delete(seccion)' lo marca para ser eliminado de la base de datos.
        #OJO: no lo elimina, solo prepara la "transacción" para ser confirmada la eliminación
        # 'delete(seccion)' es un método de la "sesión".
        db.session.delete(seccion)
        
        #'db.session.commit()' Finaliza la "transacción" ejecuta el comando SQL para ELIMINAR el registro en la base de datos.
        db.session.commit() #En pocas palabras: esta línea es la que elmina el registro de la  base de datos.
        
        #Mensaje de confirmación se va a mostrar:
        return jsonify({'message': f'Sección {id} fue eliminado con éxito'})
    except Exception as e:
        #"db.session.rollback()": Deshace todos los cambios no confirmados hechos en la sesión actual.
        db.session.rollback() #Esta es una FUNCION de SQLAlchemy.
        #Retornará un mensaje de error, indicando que es un error 500 (Error Interno del Servidor)
        return jsonify({'error': str(e)}), 500 #"'error': str(e)" captura el mensaje de error generado por la excepción ocurrida.