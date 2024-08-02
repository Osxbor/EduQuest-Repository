from flask_login import UserMixin
from .. import db

class Usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

#__repr__ es un método de Python para representar instancias de la clase Especialidades, es una forma "formal" para definir las instancias
#Se utilizó este método específicamente para tener una representación del objeto fácil de leer para el depurador
    def __repr__(self): #self se refiere a la instancia (objeto) actual de Especialidades, como llamarlo.
        #La f'<String>' Es una CADENA FORMATEADA se encarga de "construir" la representación del objeto. 
        #{self.nombre} accede al tributo nombre de la clase Especialidades, con el fin de tener (cosntruir) una representación personalizada
        #del objeto, tomando info específica sobre el propio objeto.
        return f'<solicitudes {self.nombre}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def get_id(self):
        return self.id