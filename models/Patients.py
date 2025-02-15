from models import db
from datetime import date

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    cartao_sus = db.Column(db.String(100), nullable=False)

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
