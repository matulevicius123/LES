import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from models import User  # Certifique-se de que o modelo User está importado corretamente

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Limpa o banco de dados
        db.create_all()  # Cria todas as tabelas
        # Adiciona um usuário de teste
        test_user = User(
            username='testuser',
            email='test@example.com',
            password=generate_password_hash('testpassword')  # Gera um hash para a senha
        )
        db.session.add(test_user)
        db.session.commit()

def test_login_get(client):
    response = client.get('/login')  # Simula um GET para a rota de login
    assert response.status_code == 200  # Verifica se a resposta é 200
    assert 'Login' in response.data.decode('utf-8')  # Verifica se a página contém "Login"

def test_login_post_valid(client, init_database):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })  # Simula um POST com credenciais válidas
    assert response.status_code == 302  # Verifica se a resposta é um redirecionamento (302)
    assert response.location == url_for('home', _external=True)  # Verifica se redireciona para a página inicial

def test_login_post_invalid(client):
    response = client.post('/login', data={
        'username': 'invaliduser',
        'password': 'wrongpassword'
    })  # Simula um POST com credenciais inválidas
    assert response.status_code == 200  # Verifica se a resposta é 200
    assert b'Nome de usuário ou senha incorretos' in response.data  # Verifica se a mensagem de erro está presente
