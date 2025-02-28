from models import db
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime,date

class Solicitacoes(db.Model):
    __tablename__ = 'solicitacoes'

    id: Mapped[int] = mapped_column(primary_key=True)
    motivo:Mapped[str]
    paciente_id:Mapped[int] = mapped_column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    paciente_nome:Mapped[str]
    cartao_sus:Mapped[str]
    medico_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data: Mapped[date]
    hora:Mapped[str]
    status: Mapped[str] = mapped_column(Enum('pendente', 'agendada', 'recusada','cancelada'), default='pendente')
    