import pytest
from flask import url_for
from app import app as flask_app  # Importa o app do seu arquivo
from extensions import db
from models import User

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usar banco de dados em memória para testes
    with flask_app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados de teste
        yield flask_app
        db.session.remove()
        db.drop_all()  # Remove as tabelas após os testes

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_get(client):
    response = client.get(url_for('login'))  # Faz um GET na rota de login
    assert response.status_code == 200
    assert 'Login' in response.data.decode('utf-8')  # Verifica se a página contém o texto 'Login'

def test_login_post_invalid(client):
    # Simula um POST com dados inválidos
    response = client.post(url_for('login'), data={
        'username': 'invalid_user',
        'password': 'invalid_password'
    })
    assert response.status_code == 200
    assert 'Nome de usuário ou senha incorretos' in response.data.decode('utf-8')  # Verifica a mensagem de erro

def test_home_redirects_when_not_logged_in(client):
    response = client.get(url_for('home'))
    assert response.status_code == 302  # Redireciona quando o usuário não está autenticado
    assert '/login?next=%2F' in response.headers['Location']  # Verifica se redireciona para a página de login
