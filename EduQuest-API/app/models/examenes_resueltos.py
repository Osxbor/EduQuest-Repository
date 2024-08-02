from .. import db
from sqlalchemy import TIMESTAMP
from datetime import datetime

class ExamenesResueltos(db.Model):
    __tablename__ = 'examenes_realizados'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id', ondelete='CASCADE'), nullable=False)
    puntaje_obtenido = db.Column(db.Integer, nullable=True, default=0)
    fecha_entregado = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    completado = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    def __repr__(self):
        return f'<ExamenesResueltos {self.id}>'
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
