from flask import Flask, render_template
from models import db,User
from controllers import users
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'Popofilo'

db.init_app(app)

with app.app_context():
        db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
        return User.get(user_id)


app.register_blueprint(users.bp)

@app.route('/')
def index():
        return render_template('index.html')

