from models import db

class MedicoEspecialidade(db.Model):
    __tablename__ = 'medico_especialidades'
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    especialidade_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=False)
