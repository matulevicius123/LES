import pytest
from flask import Flask

# Create a simple Flask application for testing
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

# A basic test function to check if the application is running
def test_hello(client):
    response = client.get('/')
    assert response.data == b'Hello, World!'
    assert response.status_code == 200
