from models import db
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Consulta(db.Model):
    __tablename__ = 'consultas'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_paciente:Mapped[str]
    cartao_sus: Mapped[str] 
    medico_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    paciente_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data: Mapped[datetime]
    status: Mapped[str] = mapped_column(Enum('pendente', 'confirmada', 'cancelada'), default='pendente')
    motivo: Mapped[str] 