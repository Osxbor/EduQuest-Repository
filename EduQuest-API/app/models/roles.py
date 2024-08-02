from .. import db
from sqlalchemy import TIMESTAMP
from datetime import datetime

class Roles(db.Model):
 __tablename__ = 'roles'
 id = db.Column(db.Integer, primary_key=True, autoincrement=True)
 nombre = db.Column(db.String(50), nullable=False)
 created_at = db.Column(db.DateTime, default=datetime.utcnow)
 updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 deleted_at = db.Column(db.DateTime, nullable=True)
    
def __repr__(self):
    return f'<roles {self.nombre}>'

def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}