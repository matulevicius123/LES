import pytest
from app import create_app  # Função que cria sua aplicação Flask
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

# Fixture que cria a aplicação
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,  # Modo de teste
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Banco de dados em memória
        "WTF_CSRF_ENABLED": False  # Desativar o CSRF para testes
    })

    with app.app_context():
        db.create_all()  # Cria o banco de dados em memória

        # Adicionar um usuário de teste para simulação de login
        user = User(username='testuser', password=generate_password_hash('testpassword'))
        db.session.add(user)
        db.session.commit()

    yield app

    # Finalização após os testes
    with app.app_context():
        db.session.remove()
        db.drop_all()

# Fixture que cria o cliente de teste
@pytest.fixture
def client(app):
    return app.test_client()

# Teste GET da página de login
def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

# Teste POST válido para login
def test_login_post_valid(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Redireciona em caso de sucesso

# Teste POST inválido para login
def test_login_post_invalid(client):
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200  # Retorna à página de login
    assert 'Nome de usuário ou senha incorretos' in response.data.decode('utf-8')  # Verifica se a mensagem de erro está presente
