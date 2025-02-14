from flask import Blueprint, render_template,redirect,url_for,request,flash
from models.user import Users
from models import User,db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('user',__name__, url_prefix='/user')


@bp.route('/cadastro',methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        telefone = request.form['telefone']
        user = Users(nome,email,senha_hash,telefone)
        user_existente = db.session.execute(db.select(User).filter_by(usu_email=email)).scalar_one_or_none()
        if user_existente:
            flash('Email já cadastrado')
            return redirect(url_for('user.cadastro'))
        user.save()
        return redirect(url_for('index'))
    return render_template('user/cadastro.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = db.session.execute(db.select(User).filter_by(usu_email=email)).scalar_one_or_none()
        if user and check_password_hash(user.usu_senha, senha):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Credenciais inválidas.')

    return render_template('user/login.html')

@bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))