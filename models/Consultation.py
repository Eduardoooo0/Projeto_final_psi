from models import db
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

class Consulta(db.Model):
    __tablename__ = 'consultas'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_paciente: Mapped[str]
    nome_medico: Mapped[str]
    cartao_sus: Mapped[str]
    medico_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    paciente_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    status: Mapped[str] = mapped_column(Enum('pendente', 'confirmada', 'cancelada'), default='pendente')
    motivo: Mapped[str]
    data: Mapped[date]

    def __init__(self, nome_paciente, nome_medico, cartao_sus, medico_id, paciente_id, status, motivo, data=None):
        self.nome_paciente = nome_paciente
        self.nome_medico = nome_medico
        self.cartao_sus = cartao_sus
        self.medico_id = medico_id
        self.paciente_id = paciente_id
        self.status = status
        self.motivo = motivo
        self.data = data
