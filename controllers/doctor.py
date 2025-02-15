from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db
from models.Doctor import Medico

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/medicos', methods=['GET', 'POST'])
def manage_medicos():
    if request.method == 'POST':
        especialidade = request.form.get('especialidade')
        crm = request.form.get('crm')
        new_medico = Medico(especialidade=especialidade, crm=crm)
        db.session.add(new_medico)
        db.session.commit()
        flash('Médico adicionado com sucesso!')
        return redirect(url_for('doctor.manage_medicos'))
    
    medicos = Medico.query.all()
    return render_template('medicos.html', medicos=medicos)

@doctor_bp.route('/medicos/edit/<int:id>', methods=['GET', 'POST'])
def edit_medico(id):
    medico = Medico.query.get_or_404(id)
    if request.method == 'POST':
        medico.especialidade = request.form.get('especialidade')
        medico.crm = request.form.get('crm')
        db.session.commit()
        flash('Médico atualizado com sucesso!')
        return redirect(url_for('doctor.manage_medicos'))
    
    return render_template('edit_medico.html', medico=medico)

@doctor_bp.route('/medicos/delete/<int:id>', methods=['POST'])
def delete_medico(id):
    medico = Medico.query.get_or_404(id)
    db.session.delete(medico)
    db.session.commit()
    flash('Médico deletado com sucesso!')
    return redirect(url_for('doctor.manage_medicos'))
