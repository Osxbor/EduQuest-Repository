from .. import db
from sqlalchemy import TIMESTAMP
from datetime import datetime

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'))
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'))
    seccion_id = db.Column(db.Integer, db.ForeignKey('secciones.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Alumnos {self.id}>'
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}