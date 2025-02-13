from flask import Blueprint, render_template,redirect,url_for,request,flash
from models.user import Users
from models import User,db
from flask_login import login_user, login_required, logout_user, current_user

bp = Blueprint('user',__name__, url_prefix='/user')




@bp.route('/cadastro',methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']
        user = Users(nome,email,senha,telefone)
        user_existente = db.session.execute(db.select(User).filter_by(usu_email=email)).scalar_one_or_none()
        if user_existente:
            flash('Email já cadastrado')
            return redirect(url_for('user.cadastro'))
        user.save()
        return redirect(url_for('index'))
    return render_template('user/cadastro.html')

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = db.session.execute(db.select(User).filter_by(usu_email=email)).scalar_one_or_none()
        if user:
            user = {'email':user.usu_email,'senha':user.usu_senha}
            if email == user['email'] and senha == user['senha']:
                return 'tudo certo'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('user/login.html')
