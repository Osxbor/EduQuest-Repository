from .. import db
from sqlalchemy import TIMESTAMP
from datetime import datetime

class Asignaciones(db.Model):
    __tablename__ = 'asignaciones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maestro_id = db.Column(db.Integer, db.ForeignKey('maestros.id'), nullable=False)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'), nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
    seccion_id = db.Column(db.Integer, db.ForeignKey('secciones.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Asignaciones {self.id}>'
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}