from .. import db
from sqlalchemy import TIMESTAMP
from datetime import datetime

class Examenes(db.Model):
    __tablename__ = 'examenes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_examen = db.Column(db.String(30))
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'))
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    seccion_id = db.Column(db.Integer, db.ForeignKey('secciones.id'))
    cantidad_preguntas = db.Column(db.Integer)
    puntaje_total = db.Column(db.Integer)
    fecha_publicacion = db.Column(db.Date)
    fecha_entrega = db.Column(db.Date)
    estado = db.Column(db.Boolean, default=False)
    aproved = db.Column(db.Boolean, default=False)
    comentario = db.Column(db.String(100))

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
    deleted_at = db.Column(TIMESTAMP, nullable=True)

#__repr__ es un método de Python para representar instancias de la clase Examenes, es una forma "formal" para definir las instancias
#Se utilizó este método específicamente para tener una representación del objeto fácil de leer para el depurador
    def __repr__(self):#self se refiere a la instancia (objeto) actual de Examenes, como llamarlo.
        #La f'<String>' Es una CADENA FORMATEADA se encarga de "construir" la representación del objeto. 
        #{self.nombre_examen_examen} accede al tributo nombre de la clase Examenes, con el fin de tener (cosntruir) una representación personalizada
        #del objeto, tomando info específica sobre el propio objeto.
        return f'<Examenes {self.id}>'