from models import db
from sqlalchemy import Enum

class Consulta(db.Model):
    __tablename__ = 'consultas'
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    horario_id = db.Column(db.Integer, db.ForeignKey('horarios_disponiveis.id'), nullable=False)
    status = db.Column(db.Enum('pendente', 'confirmada', 'cancelada'), default='pendente')
    motivo = db.Column(db.Text, nullable=True)
