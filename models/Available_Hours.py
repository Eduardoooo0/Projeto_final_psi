from models import db
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class HorarioDisponivel(db.Model):
    __tablename__ = 'horarios_disponiveis'

    id: Mapped[int] = mapped_column(primary_key=True)
    medico_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    data_hora_inicio: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    data_hora_fim: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    status: Mapped[str] = mapped_column(Enum('livre', 'ocupado'), default='livre')