from models import db

class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    crm = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, especialidade, crm):
        self.user_id = user_id
        self.especialidade = especialidade
        self.crm = crm

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'especialidade': self.especialidade,
            'crm': self.crm
        }
