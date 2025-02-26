from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.Doctor import Medico
from models.Patients import Paciente
from models.Consultation import Consulta
from flask_login import current_user, login_required


doctor_bp = Blueprint('doctor', __name__)
@login_required
@doctor_bp.route('/cadastrar_consultas', methods=['GET', 'POST'])

def cadastrar_consultas():
    if request.method == 'POST':
        cartao = request.form['cartao']
        status = request.form.get('status')
        motivo = request.form['motivo']
        paciente = db.session.query(Paciente).filter_by(cartao_sus=cartao).first()
        medico = db.session.query(Medico).filter_by(user_id=current_user.id).first()

        nova_consulta = Consulta(nome_paciente = paciente.nome,cartao_sus=cartao,medico_id=medico.id,paciente_id=paciente.id,status=status,motivo=motivo)
        db.session.add(nova_consulta)
        db.session.commit()
        return redirect(url_for('user.dashboard'))


    if current_user.tipo != 'medico':
        return redirect(url_for('user.dashboard'))
    return render_template('cadastrar_consultas.html')

@doctor_bp.route('/consultas',methods=['POST','GET'])
def consultas():
    if request.method == 'POST':
        pass
    dados = db.session.query(Consulta).all()
    return render_template('consultas.html',dados=dados)



@doctor_bp.route('/medicos/edit/<int:id>', methods=['GET', 'POST'])
def edit_medico(id):
    medico = Medico.query.get_or_404(id)
    if request.method == 'POST':
        medico.especialidade = request.form.get('especialidade')
        medico.crm = request.form.get('crm')
        db.session.commit()
        flash('Médico atualizado com sucesso!')
        return redirect(url_for('doctor.manage_medicos'))
    
    return render_template('edit_medico.html', medico=medico)

@doctor_bp.route('/medicos/delete/<int:id>', methods=['POST'])
def delete_medico(id):
    medico = Medico.query.get_or_404(id)
    db.session.delete(medico)
    db.session.commit()
    flash('Médico deletado com sucesso!')
    return redirect(url_for('doctor.manage_medicos'))
