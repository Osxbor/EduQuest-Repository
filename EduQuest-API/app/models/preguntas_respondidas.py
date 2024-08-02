from .. import db
from datetime import datetime

class PreguntaRespondida(db.Model):
    __tablename__ = 'preguntas_respondidas'

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id', ondelete='CASCADE'), nullable=False)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'), nullable=False)
    respuesta_id = db.Column(db.Integer, db.ForeignKey('respuestas.id'), nullable=True)
    es_correcta = db.Column(db.Boolean, default=False)
    puntos_obtenidos = db.Column(db.Numeric(10, 2), default=0.0)

    def __init__(self, examen_id, alumno_id, pregunta_id, respuesta_id, es_correcta, puntos_obtenidos, respondida):
        self.examen_id = examen_id
        self.alumno_id = alumno_id
        self.pregunta_id = pregunta_id
        self.respuesta_id = respuesta_id
        self.es_correcta = es_correcta
        self.puntos_obtenidos = puntos_obtenidos
        self.respondida = respondida
