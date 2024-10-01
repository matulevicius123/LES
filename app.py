from flask import Flask
from routes import init_routes

app = Flask(__name__)

# Defina uma chave secreta segura para proteção CSRF
app.config['SECRET_KEY'] = 'teste'

# Inicializa as rotas
init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)