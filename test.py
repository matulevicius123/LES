import pytest
from flask import url_for
from testapp import testapp as flask_app  # Importa o app do seu arquivo
from extensions import db
from models import User

@pytest.fixture
def app():
    with flask_app.app_context():
        db.create_all()  # Create tables in the in-memory database
        yield flask_app  # Yield the test app for testing
        db.session.remove()  # Remove any sessions
        db.drop_all()  # Drop all tables after the tests are done

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_get(client):
    response = client.get(url_for('login'))  # Faz um GET na rota de login
        assert b"Criar uma nova conta" in response.data

def test_login_post_invalid(client):
 # Simula um POST com dados inválidos
    response = client.post(url_for('login'), data={
        'username': 'invalid_user',
        'password': 'invalid_password'
    })
    assert response.status_code == 200  # A página de login deve ser retornada

    # Testando o método check_password para o usuário válido
    user = User.query.filter_by(username='test_user').first()
    assert user.check_password('valid_password') is True  # Deve retornar True para a senha correta
    assert user.check_password('wrong_password') is False  # Deve retornar False para a senha incorreta

