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
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        tipo = request.form['tipo']

        novo_usuario = User(nome=nome, email=email, senha=senha, tipo=tipo)
        db.session.add(novo_usuario)
        db.session.commit() 

        

        if tipo == 'medico':
            especialidade = request.form['especialidade']  
            crm = request.form['crm']  
            novo_medico = Medico(user_id=novo_usuario.id, especialidade=especialidade, crm=crm)
            db.session.add(novo_medico)

       
        elif tipo == 'paciente':
            idade = int(request.form['idade'])  
            data_nascimento_str = request.form['data_nascimento']  # Campo de data de nascimento
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()  # Converter string para date
            telefone = request.form['telefone']  
            endereco = request.form['endereco']  
            cartao_sus = request.form['cartao_sus']  
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


    medicos = Medico.query.filter_by(user_id=id).all()
    for medico in medicos:
        db.session.delete(medico)


    db.session.delete(usuario)
    db.session.commit()
    
    flash('Usuário deletado com sucesso!', 'success')
    return redirect(url_for('admin.dashboard'))