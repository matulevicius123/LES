# app.py
from flask import Flask
from extensions import db, login_manager  # Importa as extensões inicializadas
from routes import init_routes
from models import User  # Importa o modelo de usuário para a função user_loader

# Configurações do aplicativo Flask
app = Flask(__name__)

# Defina uma chave secreta segura para proteção CSRF
app.config['SECRET_KEY'] = 'sua-chave-secreta-super-segura'

# Configurações de banco de dados para MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ejv2024#@98.82.226.137/ejv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa as extensões com a instância do aplicativo Flask
db.init_app(app)
login_manager.init_app(app)

# Define a rota de login padrão para usuários não autenticados
login_manager.login_view = 'login'

# Função para carregar o usuário com base no ID armazenado na sessão
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importa e inicializa as rotas
init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
