from models import db
from sqlalchemy.orm import Mapped, mapped_column

class Especialidade(db.Model):
    __tablename__ = 'especialidades'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] 
    descricao: Mapped[str] 