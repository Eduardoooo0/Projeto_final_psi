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
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')

        if tipo == 'medico':
            senha = os.getenv('SENHA_PADRAO')
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
        elif tipo is None:
            hash_senha = generate_password_hash(senha)
            novo_user = User(nome=nome, email=email, senha=hash_senha, tipo='paciente')
            db.session.add(novo_user)
            db.session.commit()

            idade = request.form.get('idade')
            data_nascimento = datetime.strptime(request.form.get('data_nascimento'), '%Y-%m-%d').date()
            telefone = request.form.get('telefone')
            endereco = request.form.get('endereco')
            cartao_sus = request.form.get('cartao_sus')
            novo_paciente = Paciente(user_id=novo_user.id, nome=nome, idade=idade, data_nascimento=data_nascimento,
                                    telefone=telefone, endereco=endereco, cartao_sus=cartao_sus)
            db.session.add(novo_paciente)

        db.session.commit()
        flash('Usuário registrado com sucesso!')
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
            return redirect(url_for('user.dashboard'))
        flash('Credenciais inválidas')
        return redirect(url_for('user.login'))
    return render_template('login.html')

@user_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!')
    return redirect(url_for('user.login'))

@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('home.html')

@user_bp.route('/editar_senha', methods=['POST','GET'])
def editar_senha():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = db.session.query(User).filter_by(email=email).first()
        nova_senha = generate_password_hash(senha)
        user.senha = nova_senha
        db.session.commit()
        return redirect(url_for('user.login'))

    return render_template('editar_senha.html')