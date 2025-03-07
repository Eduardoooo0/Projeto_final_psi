from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.Doctor import Medico
from models.Patients import Paciente
from models.Consultation import Consulta
from models.Solicitations import Solicitacoes
from models.user import User
from flask_login import current_user, login_required
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__)

from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.Doctor import Medico
from models.Patients import Paciente
from models.Consultation import Consulta
from models.Solicitations import Solicitacoes
from models.user import User
from flask_login import current_user, login_required
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__)

from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.Doctor import Medico
from models.Patients import Paciente
from models.Consultation import Consulta
from models.Solicitations import Solicitacoes
from models.user import User
from flask_login import current_user, login_required
from datetime import datetime

doctor_bp = Blueprint('doctor', __name__)

@login_required
@doctor_bp.route('/cadastrar_consultas', methods=['GET', 'POST'])
def cadastrar_consultas():
    if current_user.tipo != 'medico':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        cartao = request.form.get('cartao')
        status = request.form.get('status')
        motivo = request.form.get('motivo')
        data = request.form.get('data')

        if not cartao or not status or not motivo or not data:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('doctor.cadastrar_consultas'))

        try:
            data = datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            flash('Data inválida.', 'danger')
            return redirect(url_for('doctor.cadastrar_consultas'))

        paciente = db.session.query(Paciente).filter_by(cartao_sus=cartao).first()
        medico = db.session.query(Medico).filter_by(user_id=current_user.id).first()

        if not paciente:
            flash('Paciente não encontrado.', 'danger')
            return redirect(url_for('doctor.cadastrar_consultas'))

        if not medico:
            flash('Médico não encontrado.', 'danger')
            return redirect(url_for('doctor.cadastrar_consultas'))

        nova_consulta = Consulta(
            nome_paciente=paciente.nome,
            nome_medico=current_user.nome,
            cartao_sus=cartao,
            medico_id=medico.id,
            paciente_id=paciente.id,
            status=status,
            motivo=motivo,
            data=data
        )
        db.session.add(nova_consulta)
        db.session.commit()
        flash('Consulta cadastrada com sucesso!', 'success')
        return redirect(url_for('doctor.consultas'))

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
        data_string = request.form.get('data')
        if data_string:
            try:
                consulta.data = datetime.strptime(data_string, '%Y-%m-%d')
            except ValueError:
                flash('Data inválida.', 'danger')
                return redirect(url_for('doctor.edit_consulta', id=id))
        consulta.motivo = request.form.get('motivo')
        consulta.status = request.form.get('status')
        db.session.commit()
        flash('Consulta atualizada com sucesso!', 'success')
        return redirect(url_for('doctor.consultas'))

    return render_template('editar_consulta.html', consulta=consulta)

@doctor_bp.route('/consultas/confirm/<int:id>', methods=['POST'])
@login_required
def confirm_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    consulta.status = 'confirmada'
    db.session.commit()
    flash('Consulta concluída com sucesso!', 'success')
    return redirect(url_for('doctor.consultas'))

@doctor_bp.route('/consultas/cancelar/<int:id>', methods=['POST'])
@login_required
def cancelar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    consulta.status = 'cancelada'
    db.session.commit()
    flash('Consulta cancelada com sucesso!', 'success')
    return redirect(url_for('doctor.consultas'))

@doctor_bp.route('/consultas', methods=['GET'])
@login_required
def consultas():
    medico = db.session.query(Medico).filter_by(user_id=current_user.id).first()
    dados = db.session.query(Consulta).filter_by(medico_id=medico.id).all()
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

@doctor_bp.route('/agenda', methods=['GET'])
@login_required
def agenda():
    medico = db.session.query(Medico).filter_by(user_id=current_user.id).first()
    solicitacoes = db.session.query(Solicitacoes).filter_by(medico_id=medico.id).all()
    return render_template('agenda.html', solicitacoes=solicitacoes)

@doctor_bp.route('/solicitacoes/recusar/<int:id>', methods=['POST'])
@login_required
def recusar_solicitacao(id):
    solicitacao = Solicitacoes.query.get_or_404(id)
    paciente_id = solicitacao.paciente_id
    paciente = db.session.query(Paciente).filter_by(id=paciente_id).first()
    user = db.session.query(User).filter_by(id=paciente.user_id).first()
    solicitacao.status = 'recusada'
    db.session.commit()
    mensagem = 'Infelizmente não foi possível agendar sua consulta.'
    Medico.invite_email_for_user(email=user.email, status='recusada', mensagem=mensagem)
    return redirect(url_for('doctor.agenda'))

@doctor_bp.route('/solicitacoes/agendar/<int:id>', methods=['POST'])
@login_required
def agendar_solicitacao(id):
    solicitacao = Solicitacoes.query.get_or_404(id)
    paciente_id = solicitacao.paciente_id
    paciente = db.session.query(Paciente).filter_by(id=paciente_id).first()
    user = db.session.query(User).filter_by(id=paciente.user_id).first()
    solicitacao.status = 'agendada'
    db.session.commit()
    mensagem = 'Agendamento feito com sucesso.'
    Medico.invite_email_for_user(email=user.email, status='agendada', mensagem=mensagem)
    return redirect(url_for('doctor.agenda'))

@doctor_bp.route('/solicitacoes/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_solicitacao(id):
    solicitacao = Solicitacoes.query.get_or_404(id)
    db.session.delete(solicitacao)
    db.session.commit()
    return redirect(url_for('doctor.agenda'))

@doctor_bp.route('/solicitacoes/cancelar/<int:id>', methods=['POST'])
@login_required
def desagendar_solicitacao(id):
    solicitacao = Solicitacoes.query.get_or_404(id)
    paciente_id = solicitacao.paciente_id
    paciente = db.session.query(Paciente).filter_by(id=paciente_id).first()
    user = db.session.query(User).filter_by(id=paciente.user_id).first()
    solicitacao.status = 'cancelada'
    db.session.commit()
    mensagem = 'Infelizmente seu agendamento precisou ser cancelado.'
    Medico.invite_email_for_user(email=user.email, status='cancelada', mensagem=mensagem)
    return redirect(url_for('doctor.agenda'))
