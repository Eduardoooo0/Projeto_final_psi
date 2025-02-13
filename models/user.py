from models import User,db
from sqlalchemy import select


class Users:
    def __init__(self,nome,email,senha,telefone):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
    
    def save(self):
        self.user = User(usu_nome=self.nome,usu_email=self.email,usu_senha=self.senha,usu_telefone=self.telefone)
        db.session.add(self.user)
        db.session.commit()