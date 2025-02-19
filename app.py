from flask import Flask, render_template
from models import db
from models.user import User
from controllers.user import user_bp
from controllers.doctor import doctor_bp
from controllers.patients import patients_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'xoxorroxupetao'

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
    return render_template('index.html')

