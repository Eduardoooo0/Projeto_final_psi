from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.Patients import Paciente
from models.Solicitations import Solicitacoes
from models.Consultation import Consulta
from models.Doctor import Medico
from models.user import User
from datetime import datetime
from flask_login import current_user, login_required

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/pacientes', methods=['GET', 'POST'])
def manage_pacientes():
    if request.method == 'POST':
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        data_nascimento = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        cartao_sus = request.form.get('cartao_sus')

        if not nome or not idade or not data_nascimento or not telefone or not endereco or not cartao_sus:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('patients.manage_pacientes'))

        if Paciente.query.filter_by(cartao_sus=cartao_sus).first():
            flash('Cartão SUS já registrado.', 'danger')
            return redirect(url_for('patients.manage_pacientes'))

        try:
            data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        except ValueError:
            flash('Data de nascimento inválida.', 'danger')
            return redirect(url_for('patients.manage_pacientes'))

        novo_paciente = Paciente(
            nome=nome, idade=idade, data_nascimento=data_nascimento,
            telefone=telefone, endereco=endereco, cartao_sus=cartao_sus
        )
        db.session.add(novo_paciente)
        db.session.commit()
        flash('Paciente adicionado com sucesso!', 'success')
        return redirect(url_for('patients.manage_pacientes'))
    
    pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

@patients_bp.route('/pacientes/edit/<int:id>', methods=['GET', 'POST'])
def edit_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    if request.method == 'POST':
        paciente.nome = request.form.get('nome')
        paciente.idade = request.form.get('idade')
        data_nascimento = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        cartao_sus = request.form.get('cartao_sus')

        if not paciente.nome or not paciente.idade or not data_nascimento or not telefone or not endereco or not cartao_sus:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('patients.edit_paciente', id=id))

        if Paciente.query.filter(Paciente.id != id).filter_by(cartao_sus=cartao_sus).first():
            flash('Cartão SUS já registrado.', 'danger')
            return redirect(url_for('patients.edit_paciente', id=id))

        try:
            paciente.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        except ValueError:
            flash('Data de nascimento inválida.', 'danger')
            return redirect(url_for('patients.edit_paciente', id=id))

        paciente.telefone = telefone
        paciente.endereco = endereco
        paciente.cartao_sus = cartao_sus
        db.session.commit()
        flash('Paciente atualizado com sucesso!', 'success')
        return redirect(url_for('patients.manage_pacientes'))
    
    return render_template('edit_paciente.html', paciente=paciente)

@patients_bp.route('/pacientes/delete/<int:id>', methods=['POST'])
def delete_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente deletado com sucesso!', 'success')
    return redirect(url_for('patients.manage_pacientes'))

@patients_bp.route('/paciente/consultas', methods=['GET'])
@login_required
def listar_consultas():
    paciente = Paciente.query.filter_by(user_id=current_user.id).first()
    if not paciente:
        flash('Paciente não encontrado.', 'danger')
        return redirect(url_for('user.dashboard'))
    consultas = Consulta.query.filter_by(paciente_id=paciente.id).all()
    return render_template('listar_consultas.html', consultas=consultas)

@patients_bp.route('/solicitar_consulta', methods=['GET', 'POST'])
@login_required
def solicitar_consulta():
    if request.method == 'POST':
        motivo = request.form.get('motivo')
        cartao = request.form.get('cartao')
        medico_id = request.form.get('medico_id')
        data = request.form.get('data')
        hora = request.form.get('hora')

        if not motivo or not cartao or not medico_id or not data or not hora:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('patients.solicitar_consulta'))

        try:
            data = datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            flash('Data inválida.', 'danger')
            return redirect(url_for('patients.solicitar_consulta'))

        paciente = Paciente.query.filter_by(cartao_sus=cartao).first()
        medico = Medico.query.get(medico_id)
        
        if not paciente:
            flash('Paciente não encontrado.', 'danger')
            return redirect(url_for('patients.solicitar_consulta'))

        if not medico:
            flash('Médico não encontrado.', 'danger')
            return redirect(url_for('patients.solicitar_consulta'))

        solicitacao = Solicitacoes(
            paciente_nome=paciente.nome,
            cartao_sus=paciente.cartao_sus,
            medico_id=medico_id,
            paciente_id=paciente.id,
            status='pendente',
            motivo=motivo,
            data=data,
            hora=hora
        )
        db.session.add(solicitacao)
        db.session.commit()
        flash('Consulta solicitada com sucesso!', 'success')
        return redirect(url_for('patients.listar_consultas'))

    medicos = Medico.query.all()
    return render_template('solicitar_consulta.html', medicos=medicos)
