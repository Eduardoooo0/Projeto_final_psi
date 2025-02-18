from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.Patients import Paciente

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
        flash('Paciente adicionado com sucesso!')
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
        flash('Paciente atualizado com sucesso!')
        return redirect(url_for('patients.manage_pacientes'))
    
    return render_template('edit_paciente.html', paciente=paciente)

@patients_bp.route('/pacientes/delete/<int:id>', methods=['POST'])
def delete_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente deletado com sucesso!')
    return redirect(url_for('patients.manage_pacientes'))
