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
        paciente.data_nascimento = request.form.get('data_nascimento')
        paciente.telefone = request.form.get('telefone')
        paciente.endereco = request.form.get('endereco')
        paciente.cartao_sus = request.form.get('cartao_sus')
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
    consultas = Consulta.query.filter_by(paciente_id=paciente.id).all() if paciente else []
    return render_template('listar_consultas.html', consultas=consultas)


@patients_bp.route('/solicitar_consulta', methods=['GET', 'POST'])
@login_required
def solicitar_consulta():
    if request.method == 'POST':
        motivo = request.form['motivo']
        medico_id = request.form['medico_id']
        data = request.form['data']
        hora= request.form['hora']
        paciente = Paciente.query.filter_by(user_id=current_user.id).first()
        medico = Medico.query.get(medico_id)
        if paciente and medico:
            solicitacao = Solicitacoes(
                paciente_nome=paciente.nome,
                cartao_sus=paciente.cartao_sus,
                medico_id=medico_id,
                paciente_id=paciente.id,
                status='pendente',
                motivo=motivo,
                data=datetime.strptime(data, '%Y-%m-%d').date(),
                hora=hora
            )
            db.session.add(solicitacao)
            db.session.commit()
            flash('Consulta solicitada com sucesso!', 'success')
            return redirect(url_for('patients.listar_consultas'))

    # Renderiza o formulário para solicitar uma consulta
    medicos = Medico.query.all()
    return render_template('solicitar_consulta.html', medicos=medicos)


