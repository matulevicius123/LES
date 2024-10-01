# app.py
from flask import Flask
from extensions import db, login_manager
from routes import init_routes  # Importar após inicializar as extensões

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'teste'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ejv2024#@98.82.226.137/ejv'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)

    # Inicializar rotas
    init_routes(app)

    # Configurar o carregador de usuários para Flask-Login
    from models import User  # Importar aqui para evitar circular import

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


