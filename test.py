import pytest
from flask import url_for
from testapp import testapp as flask_app  # Importa o app do seu arquivo
from extensions import db
from models import User
from models import CadastroInicial
from forms import PrimeiroAcessoForm

def extract_csrf_token(html):
    # Find the start of the CSRF token
    start = html.find('"hidden" value="') + len('"hidden" value="')
    # Find the end of the CSRF token
    end = html.find('"', start)
    # Extract and return the CSRF token
    return html[start:end]


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
    response = client.get(url_for('primeiro_acesso'))
    response_data = response.data.decode()

    # extrai o token csrf
    start = response_data.find('"hidden" value="') + len('"hidden" value="')
    end = response_data.find('"', start)

    csrf_token = response_data[start:end] 

    response = client.post(url_for('primeiro_acesso'), data={
        'username': 'usuario',
        'email': 'novo_usuario@example.com',
        'password': 'supersenha',
        'repeat_password': 'supersenha',
        'csrf_token': csrf_token  
    })

    users = User.query.all()
    #print("Current users in the database:")
    #for user in users:
    #    print(f"User: {user.username}, Email: {user.email}, Password Hash: {user.password}") 
    #print(response.data.decode('utf-8'))  
    
    #print("Extracted CSRF Token:", csrf_token)  # Debugging 

    #if not form.validate():
    #    print(form.errors) 
        
    user = User.query.filter_by(username='usuario').first() 
    assert user is not None  # verificar se o usuario existe
    
def test_login_com_conta_nova(client):
    response = client.post(url_for('login'), data={
        'username': 'usuario',
        'password': 'supersenha'
    })
    
    assert response.status_code == 200 
    print("Login response status code:", response.status_code)
    print("Login response data:", response.data.decode())

def test_cadastro_valid(client):
    response = client.post(url_for('cadastro'), data={
        'nome_completo': 'Jack da Silva',
        'idade': 30,
        'renda_mensal': '5000.00',  
        'despesas_mensais': '3000.00',
        'patrimonio_atual': '10000.00',
        'idade_desejada_aposentadoria': 60,
        'renda_desejada_aposentadoria': '8000.00',
        'tolerancia_risco': 'Alto',
        'horizonte_investimentos': 'Longo prazo'
    })

    assert response.status_code == 200 #procura um redirect
    assert CadastroInicial.query.count() == 1  
    cadastro = CadastroInicial.query.first()
    assert cadastro.nome_completo == 'João da Silva'
    assert cadastro.idade == 30

