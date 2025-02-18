from models import db
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

class Consulta(db.Model):
    __tablename__ = 'consultas'

    id: Mapped[int] = mapped_column(primary_key=True)
    medico_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    paciente_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    horario_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('horarios_disponiveis.id'), nullable=False)
    status: Mapped[str] = mapped_column(Enum('pendente', 'confirmada', 'cancelada'), default='pendente')
    motivo: Mapped[str] 