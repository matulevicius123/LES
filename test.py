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
    response = client.get('/')  # Make a GET request to the home route
    assert response.status_code == 200  # Check if the status code is 200
    assert b'Home Page Content' in response.data  # Replace with actual content check

# Test the login route with GET method
def test_login_get(client):
    response = client.get('/login')  # Make a GET request to the login route
    assert response.status_code == 200  # Check if the status code is 200
    assert b'Login' in response.data  # Check for the presence of the login form

# Test the login route with POST method
def test_login_post(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })  # Simulate submitting the login form
    assert response.status_code == 200  # Check if the status code is still 200
    assert b'Login' in response.data  # Check if the login form is still rendered

    # You can also check for the presence of error messages if the login is invalid
    # Example:
    # assert b'Invalid username or password' in response.data

# Test the first access form
def test_primeiro_acesso_get(client):
    response = client.get('/primeiro_acesso')  # Assuming you have this route
    assert response.status_code == 200  # Check if the status code is 200
    assert b'Primeiro Acesso' in response.data  # Replace with actual content check

def test_primeiro_acesso_post(client):
    response = client.post('/primeiro_acesso', data={
        'nome_completo': 'Test User',
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'repeat_password': 'testpassword'
    })  # Simulate submitting the primeiro acesso form
    assert response.status_code == 200  # Check if the status code is still 200
    assert b'Welcome, Test User' in response.data  # Adjust this based on your expected outcome
