from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.user import User
from models.Consultation import Consulta
from models.Doctor import Medico
from models.Patients import Paciente
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if current_user.tipo != 'admin':
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))
    usuarios = User.query.all()
    consultas = Consulta.query.all()
    return render_template('admin_dashboard.html', usuarios=usuarios, consultas=consultas)

@admin_bp.route('/add_usuario', methods=['GET', 'POST'])
@login_required
def add_usuario():
    if current_user.tipo != 'admin':
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')

        if not nome or not email or not senha or not tipo:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('admin.add_usuario'))

        if User.query.filter_by(email=email).first():
            flash('Email já registrado.', 'danger')
            return redirect(url_for('admin.add_usuario'))

        if tipo not in ['medico', 'paciente', 'admin']:
            flash('Tipo de usuário inválido.', 'danger')
            return redirect(url_for('admin.add_usuario'))

        hash_senha = generate_password_hash(senha)
        novo_usuario = User(nome=nome, email=email, senha=hash_senha, tipo=tipo)
        db.session.add(novo_usuario)
        db.session.commit()

        if tipo == 'medico':
            especialidade = request.form.get('especialidade')
            crm = request.form.get('crm')

            if not especialidade or not crm:
                flash('Especialidade e CRM são obrigatórios para médicos.', 'danger')
                return redirect(url_for('admin.add_usuario'))

            novo_medico = Medico(user_id=novo_usuario.id, especialidade=especialidade, crm=crm)
            db.session.add(novo_medico)

        elif tipo == 'paciente':
            idade = request.form.get('idade')
            data_nascimento = request.form.get('data_nascimento')
            telefone = request.form.get('telefone')
            endereco = request.form.get('endereco')
            cartao_sus = request.form.get('cartao_sus')

            if not idade or not data_nascimento or not telefone or not endereco or not cartao_sus:
                flash('Todos os campos são obrigatórios para pacientes.', 'danger')
                return redirect(url_for('admin.add_usuario'))

            if Paciente.query.filter_by(cartao_sus=cartao_sus).first():
                flash('Cartão SUS já registrado.', 'danger')
                return redirect(url_for('admin.add_usuario'))

            try:
                data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                flash('Data de nascimento não está no formato correto.', 'danger')
                return redirect(url_for('admin.add_usuario'))

            novo_paciente = Paciente(
                user_id=novo_usuario.id,
                nome=nome,
                idade=idade,
                data_nascimento=data_nascimento,
                telefone=telefone,
                endereco=endereco,
                cartao_sus=cartao_sus
            )
            db.session.add(novo_paciente)

        db.session.commit()
        flash('Usuário adicionado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('add_usuario.html')


@admin_bp.route('/deletar_usuario/<int:id>', methods=['POST'])
@login_required
def deletar_usuario(id):
    if current_user.tipo != 'admin':
        flash('Acesso negado', 'danger')
        return redirect(url_for('index'))
    
    usuario = User.query.get_or_404(id)

    if usuario.tipo == 'admin':
        flash('Não é possível deletar um administrador.', 'danger')
        return redirect(url_for('admin.dashboard'))

    medicos = Medico.query.filter_by(user_id=id).all()
    for medico in medicos:
        db.session.delete(medico)

    pacientes = Paciente.query.filter_by(user_id=id).all()
    for paciente in pacientes:
        db.session.delete(paciente)

    db.session.delete(usuario)
    db.session.commit()
    
    flash('Usuário deletado com sucesso!', 'success')
    return redirect(url_for('admin.dashboard'))
