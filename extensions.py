from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicializa as extensões, mas ainda não as conecta ao aplicativo
db = SQLAlchemy()
login_manager = LoginManager()
