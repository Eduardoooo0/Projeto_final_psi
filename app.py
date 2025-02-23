from flask import Flask, render_template
from models import db
from models.user import User
from controllers.user import user_bp
from controllers.doctor import doctor_bp
from controllers.patients import patients_bp
from flask_login import LoginManager
import os
from werkzeug.security import generate_password_hash
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'xoxorroxupetao'

app.config['MAIL_SERVER'] = os.getenv('SERVER')
app.config['MAIL_PORT'] = int(os.getenv('PORT'))
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('USERNAME')
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(doctor_bp, url_prefix='/doctor')
app.register_blueprint(patients_bp, url_prefix='/patients')

@app.route('/')
def index():
    user = User.query.filter_by(tipo='admin').first()
    if user is None:
        user = User(nome=os.getenv('NOME_ADMIN'), email=os.getenv('EMAIL_ADMIN'), senha=generate_password_hash(os.getenv('SENHA_ADMIN')), tipo=os.getenv('TIPO_ADMIN'))
        db.session.add(user)
        db.session.commit()
    return render_template('index.html')

