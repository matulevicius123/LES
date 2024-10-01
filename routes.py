from flask import render_template
from forms import LoginForm, PrimeiroAcessoForm

def init_routes(app):
    
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        login_form = LoginForm()
        
        # Neste exemplo, não há lógica de autenticação ainda.
        return render_template('login.html', form=login_form)
