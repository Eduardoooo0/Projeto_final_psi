from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.Doctor import Medico
from models.Patients import Paciente
from models import db
from datetime import datetime
import os

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        tipo = request.form.get('tipo')

        
        if User.query.filter_by(email=email).first():
            flash('O e-mail já está em uso.', 'danger')
            return redirect(url_for('user.register'))

        if tipo == 'medico':
            senha = os.getenv('SENHA_PADRAO')
            if not senha:
                flash('A senha padrão não está definida.', 'danger')
                return redirect(url_for('user.register'))

            hash_senha = generate_password_hash(senha)
            novo_user = User(nome=nome, email=email, senha=hash_senha, tipo=tipo)
            db.session.add(novo_user)
            db.session.commit()

            User.invite_email_for_doctor(email=email)
            user = User.query.filter_by(email=email).first()
            especialidade = request.form.get('especialidade')
            crm = request.form.get('crm')
            novo_medico = Medico(user_id=user.id, especialidade=especialidade, crm=crm)
            db.session.add(novo_medico)
            db.session.commit()

        else:
            senha = request.form.get('senha')
            hash_senha = generate_password_hash(senha)
            novo_user = User(nome=nome, email=email, senha=hash_senha, tipo='paciente')
            
            idade = request.form.get('idade')
            data_nascimento = request.form.get('data_nascimento')
            telefone = request.form.get('telefone')
            endereco = request.form.get('endereco')
            cartao_sus = request.form.get('cartao_sus')

        
            if Paciente.query.filter_by(cartao_sus=cartao_sus).first():
                flash('O cartão SUS já está em uso.', 'danger')
                return redirect(url_for('user.register'))

            try:
                data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                flash('Data de nascimento não está no formato correto.', 'danger')
                return redirect(url_for('user.register'))

            db.session.add(novo_user)
            db.session.commit()


            novo_paciente = Paciente(user_id=novo_user.id, nome=nome, idade=idade,data_nascimento=data_nascimento, telefone=telefone,endereco=endereco, cartao_sus=cartao_sus)
            db.session.add(novo_paciente)
            db.session.commit()

        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            if current_user.tipo == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        flash('Credenciais inválidas', 'danger')
        return redirect(url_for('user.login'))
    return render_template('login.html')

@user_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('home.html')

@user_bp.route('/editar_senha', methods=['POST', 'GET'])
@login_required
def editar_senha():
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')

        if not nova_senha:
            flash('A nova senha é obrigatória.', 'danger')
            return redirect(url_for('user.editar_senha'))

        user = current_user
        user.senha = generate_password_hash(nova_senha)
        db.session.commit()
        flash('Senha atualizada com sucesso!', 'success')
        return redirect(url_for('user.dashboard'))

    return render_template('editar_senha.html')
