from models import db
from sqlalchemy import Enum

class HorarioDisponivel(db.Model):
    __tablename__ = 'horarios_disponiveis'
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data_hora_inicio = db.Column(db.DateTime, nullable=False)
    data_hora_fim = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('livre', 'ocupado'), default='livre')
