from models import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] 
    email: Mapped[str] 
    senha: Mapped[str] 
    tipo: Mapped[str] = mapped_column(db.Enum('admin', 'médico', 'paciente'), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return self.id