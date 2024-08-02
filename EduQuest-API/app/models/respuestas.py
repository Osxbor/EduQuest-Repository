from .. import db
from sqlalchemy import TIMESTAMP
from datetime import datetime

class Respuestas(db.Model):
    __tablename__ = 'respuestas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'))
    respuesta = db.Column(db.Text, nullable=False)
    es_correcta = db.Column(db.Boolean, nullable=False)

    #"db.TIMESTAMP": es un TIPO DE DATO del SQLAlchemy que almacena la información de la fecha y hora.
    #"server_default": es un ARGUMENTO pare DEFINIR un valor por defecto en la 
    # base de datos, se usa en la línea para ASIGNAR automáticamente la fecha y hora del servidor.
    #"db.func.current_timestamp()": FUNCIÓN de Alchemy que genera una expresión SQL para obtener la FECHA Y HORA ACTUAL DEL SERVIDOR
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    
    #"onupdate=db.func.current_timestamp()": Se asegura de que el atributo/columna se actualice 
    # atomáticamente cada que el registro se actualice (Siempre con la fecha y hora del servidor)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    #"TIMESTAMP, nullable=True" se va a encargar de marcar la fecha y hora en la que el registro fue
    #fue marcado como eliminado, sin físicamente haberlo borrado de la base de datos, de lo contrario tendrán 
    # el valor como "null"
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

#__repr__ es un método de Python para representar instancias de la clase Respuestas, es una forma "formal" para definir las instancias
#Se utilizó este método específicamente para tener una representación del objeto fácil de leer para el depurador
    def __repr__(self):#self se refiere a la instancia (objeto) actual de Respuestas, como llamarlo.
        #La f'<String>' Es una CADENA FORMATEADA se encarga de "construir" la representación del objeto. 
        #{self.nombre} accede al tributo nombre de la clase Respuestas, con el fin de tener (cosntruir) una representación personalizada
        #del objeto, tomando info específica sobre el propio objeto.
        return f'<Respuesta {self.respuesta}>'