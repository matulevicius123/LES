import pytest
from flask import url_for
from testapp import testapp as flask_app  # Importa o app do seu arquivo
from extensions import db
from models import User
from forms import PrimeiroAcessoForm


@pytest.fixture
def app():
    with flask_app.app_context():
        db.create_all() 
        yield flask_app  
        db.session.remove()  
        db.drop_all() 

@pytest.fixture
def client(app):
    return app.test_client()

# testando para a criacao de login
def test_login_get(client):
    response = client.get(url_for('login'))  # Faz um GET na rota de login
    # Havera um redirecionamento para o primeiro acesso.
    print(response.data.decode('utf-8'))  # Print the HTML response for debugging
    assert response.status_code == 200  
    assert b'<button type="submit" class="btn btn-custom btn-block text-white" name="submit_login">Login</button>' in response.data  


# testando para a criacao de conta
def test_primeiro_acesso_post_valid(client):
    response = client.post(url_for('primeiro_acesso'), data={
        'username': 'usuario',
        'email': 'novo_usuario@example.com',
        'password': 'supersenha',
        'repeat_password': 'supersenha'
    })
    print(User.query.all()) 
    print(response.data.decode('utf-8'))  # Decode to convert bytes to a string

        # Check if form validation failed
    form = PrimeiroAcessoForm(data={
        'username': 'usuario',
        'email': 'novo_usuario@example.com',
        'password': 'supersenha',
        'repeat_password': 'supersenha'
    })
    
    if not form.validate():
        print(form.errors)  # Print form errors if validation fails
        
    user = User.query.filter_by(username='usuario').first() 
    assert user is not None  # verificar se o usuario existe

