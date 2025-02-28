from models import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nome: Mapped[str] 
    idade: Mapped[int] 
    data_nascimento: Mapped[date] 
    telefone: Mapped[str] 
    endereco: Mapped[str] 
    cartao_sus: Mapped[str] 

    def __init__(self, user_id, nome, idade, data_nascimento, telefone, endereco, cartao_sus):
        self.user_id = user_id
        self.nome = nome
        self.idade = idade
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.endereco = endereco
        self.cartao_sus = cartao_sus

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nome': self.nome,
            'idade': self.idade,
            'data_nascimento': self.data_nascimento,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'cartao_sus': self.cartao_sus
        }
    
    user = relationship("User", backref="pacientes")