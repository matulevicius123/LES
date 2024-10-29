# arquivo para uma versao do app para testes, usando um banco de dados temporario e evitando conflitos
from flask import Flask
from extensions import db, login_manager
from routes import init_routes
from models import User

testapp = Flask(__name__)  
testapp.config['SECRET_KEY'] = 'sua-chave-secreta-super-segura'
testapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # banco de dados temporarios na memoria
testapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(testapp)
login_manager.init_app(testapp)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

init_routes(testapp)
