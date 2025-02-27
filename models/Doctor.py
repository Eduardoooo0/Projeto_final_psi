from models import db
from models.user import User
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Medico(db.Model):
    __tablename__ = 'medicos'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    especialidade: Mapped[str]
    crm: Mapped[str]

    def __init__(self, user_id, especialidade, crm):
        self.user_id = user_id
        self.especialidade = especialidade
        self.crm = crm

    #relacionamento para pegar o nome do medico pela tabela user
    user = relationship("User", backref="medico")

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nome': self.user.nome,
            'especialidade': self.especialidade,
            'crm': self.crm
        }