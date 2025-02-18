from models import db
from sqlalchemy.orm import Mapped, mapped_column

class MedicoEspecialidade(db.Model):
    __tablename__ = 'medico_especialidades'

    id: Mapped[int] = mapped_column(primary_key=True)
    medico_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    especialidade_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)