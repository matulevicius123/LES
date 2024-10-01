# acessa o venv para executar o codigo
import pytest
from app import app as create_app  

@pytest.fixture
def app():
    app = create_app
    app.config['TESTING'] = True  
    return app 

@pytest.fixture
def client(app):
    return app.test_client() 

# testar home
def test_home(client):
    response = client.get('/')  # teste GET do home
    assert response.status_code == 200 
    assert b'Home - Planejador Financeiro' in response.data  
    assert b'Essa é a sua página inicial.' in response.data  


# teste da pagina de login
def test_login_get(client):
    response = client.get('/login')  # pedimos um GET para a rota de login
    assert response.status_code == 200  
    assert b'Login' in response.data 


# testando o metodo POST
def test_login_post(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })  # simulando o envio do formulario
    assert response.status_code == 200  # verificando se esta tudo certo depois do retorno
