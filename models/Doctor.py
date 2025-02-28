from models import db
from models.user import User
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_mail import Message
import os
class Medico(db.Model):
    __tablename__ = 'medicos'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    especialidade: Mapped[str] = mapped_column(db.String(50))
    crm: Mapped[str] = mapped_column(db.String(20)) 
    user = relationship("User", backref="medicos")

    def __init__(self, user_id, especialidade, crm):
        self.user_id = user_id
        self.especialidade = especialidade
        self.crm = crm


    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nome': self.user.nome,
            'especialidade': self.especialidade,
            'crm': self.crm
        }
    
    @classmethod
    def invite_email_for_user(cls,email,status,mensagem):
        from app import mail
        user = User.query.filter_by(email=email).first()
        msg = Message('Solicitação de consulta - Resposta',
                sender=os.getenv('EMAIL'),
                recipients=[user.email])
        msg.body = f'Sua consulta foi {status}!\n {mensagem}'
        mail.send(msg)