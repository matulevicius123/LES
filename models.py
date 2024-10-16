from extensions import db  # Importa o db corretamente
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Adicione autoincrement=True
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class CadastroInicial(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    renda_mensal = db.Column(db.Numeric, nullable=False)
    despesas_mensais = db.Column(db.Numeric, nullable=False)
    patrimonio_atual = db.Column(db.Numeric, nullable=False)
    idade_desejada_aposentadoria = db.Column(db.Integer, nullable=False)
    renda_desejada_aposentadoria = db.Column(db.Numeric, nullable=False)
    tolerancia_risco = db.Column(db.String(50), nullable=False)
    horizonte_investimentos = db.Column(db.String(50), nullable=False)