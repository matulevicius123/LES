import random
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User  # Importar o modelo de usuário
from forms import LoginForm, PrimeiroAcessoForm
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db  # Importa o db do extensions

def init_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))  # Se o usuário já estiver logado, redireciona para a página inicial

        form = LoginForm()
        if form.validate_on_submit():
            # Buscar o usuário pelo nome de usuário
            user = User.query.filter_by(username=form.username.data).first()
            
            if user and check_password_hash(user.password, form.password.data):
                # Se o usuário for encontrado e a senha estiver correta, faz o login
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Nome de usuário ou senha incorretos', 'danger')

        return render_template('login.html', form=form)

    @app.route('/primeiro_acesso', methods=['GET', 'POST'])
    def primeiro_acesso():
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = PrimeiroAcessoForm()
        if form.validate_on_submit():
            # Verifica se o usuário ou email já existe
            existing_user = User.query.filter_by(username=form.username.data).first()
            existing_email = User.query.filter_by(email=form.email.data).first()

            if existing_user or existing_email:
                flash('Usuário ou email já cadastrado.', 'danger')
            else:
                # Criar novo usuário
                hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')

                new_user = User(
                                id = random.randint(1, 1000),
                                username=form.username.data,
                                email=form.email.data,
                                password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                flash('Conta criada com sucesso! Faça o login.', 'success')
                return redirect(url_for('login'))

        return render_template('primeiro_acesso.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    def home():
        return 'Você está logado!'
