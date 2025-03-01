from models import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum
from flask_login import UserMixin
import os
from flask_mail import Message
from flask import url_for,redirect


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] 
    email: Mapped[str] 
    senha: Mapped[str] 
    tipo: Mapped[str] = mapped_column(db.Enum('admin', 'medico', 'paciente'), default='paciente', nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return self.id
    
    @classmethod
    def invite_email_for_doctor(cls,email):
            from app import mail
            user = User.query.filter_by(email=email).first()
            msg = Message('Definir senha',
                    sender=os.getenv('EMAIL'),
                    recipients=[user.email])
            msg.body = f'Segue o link abaixo para definir sua senha de médico:\n <seu_IP>/user/editar_senha'
            mail.send(msg)