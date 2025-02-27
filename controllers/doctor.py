from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.Doctor import Medico
from models.Patients import Paciente
from models.Consultation import Consulta
from flask_login import current_user, login_required
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__)

@login_required
@doctor_bp.route('/cadastrar_consultas', methods=['GET', 'POST'])
def cadastrar_consultas():
    if current_user.tipo != 'medico':
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        cartao = request.form['cartao']
        status = request.form.get('status')
        motivo = request.form['motivo']
        paciente = db.session.query(Paciente).filter_by(cartao_sus=cartao).first()
        medico = db.session.query(Medico).filter_by(user_id=current_user.id).first()

        if paciente and medico:
            nova_consulta = Consulta(
                nome_paciente=paciente.nome,
                cartao_sus=cartao,
                medico_id=medico.id,
                paciente_id=paciente.id,
                status=status,
                motivo=motivo
            )
            db.session.add(nova_consulta)
            db.session.commit()
            flash('Consulta cadastrada com sucesso!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Paciente ou médico não encontrado.', 'danger')

    return render_template('cadastrar_consultas.html')


@doctor_bp.route('/consultas/delete/<int:id>', methods=['POST'])
@login_required
def delete_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    flash('Consulta excluída com sucesso!', 'success')
    return redirect(url_for('doctor.consultas'))


@doctor_bp.route('/consultas/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_consulta(id):
    consulta = Consulta.query.get_or_404(id)

    if request.method == 'POST':
        # Converte a string de data para um objeto datetime
        data_string = request.form.get('data')
        if data_string:
            consulta.data = datetime.strptime(data_string, '%Y-%m-%d')  # Use datetime se a coluna for DateTime
        consulta.motivo = request.form.get('motivo')
        consulta.status = request.form.get('status')
        
        db.session.commit()
        flash('Consulta atualizada com sucesso!', 'success')
        return redirect(url_for('doctor.consultas'))

    return render_template('editar_consulta.html', consulta=consulta)


@doctor_bp.route('/consultas', methods=['GET'])
@login_required
def consultas():
    dados = db.session.query(Consulta).all()
    return render_template('consultas.html', dados=dados)


@doctor_bp.route('/medicos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_medico(id):
    medico = Medico.query.get_or_404(id)
    
    if request.method == 'POST':
        medico.especialidade = request.form.get('especialidade')
        medico.crm = request.form.get('crm')
        db.session.commit()
        flash('Médico atualizado com sucesso!', 'success')
        return redirect(url_for('doctor.manage_medicos'))
    
    return render_template('edit_medico.html', medico=medico)


@doctor_bp.route('/medicos/delete/<int:id>', methods=['POST'])
@login_required
def delete_medico(id):
    medico = Medico.query.get_or_404(id)
    db.session.delete(medico)
    db.session.commit()
    flash('Médico deletado com sucesso!', 'success')
    return redirect(url_for('doctor.manage_medicos'))