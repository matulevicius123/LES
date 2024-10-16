import random
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User  # Importar o modelo de usuário
from forms import CadastroInicialForm, LoginForm, PrimeiroAcessoForm
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db  # Importa o db do extensions
from models import CadastroInicial
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
                                username=form.username.data,
                                email=form.email.data,
                                password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                flash('Conta criada com sucesso!', 'success')
                return redirect(url_for('cadastro'))

        return render_template('primeiro_acesso.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    def home():
        return render_template('home.html')  # Renderiza o template da página inicial


    def format_currency(value):
        """
        Função para remover o símbolo de moeda, separadores de milhar e converter vírgula para ponto.
        Exemplo: 'R$ 1.221.122,22' -> 1221122.22
        """
        if value:
            # Remove o símbolo de moeda e separadores de milhar
            value = value.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(value)
        return 0.0

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        form = CadastroInicialForm()
        if form.validate_on_submit():
            # Limpar os valores monetários usando a função de formatação
            renda_mensal = format_currency(form.renda_mensal.data)
            despesas_mensais = format_currency(form.despesas_mensais.data)
            patrimonio_atual = format_currency(form.patrimonio_atual.data)
            renda_desejada_aposentadoria = format_currency(form.renda_desejada_aposentadoria.data)

            # Criar novo cadastro com os valores limpos
            novo_cadastro = CadastroInicial(
                nome_completo=form.nome_completo.data,
                idade=form.idade.data,
                renda_mensal=renda_mensal,
                despesas_mensais=despesas_mensais,
                patrimonio_atual=patrimonio_atual,
                idade_desejada_aposentadoria=form.idade_desejada_aposentadoria.data,
                renda_desejada_aposentadoria=renda_desejada_aposentadoria,
                tolerancia_risco=form.tolerancia_risco.data,
                horizonte_investimentos=form.horizonte_investimentos.data
            )
            
            db.session.add(novo_cadastro)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('home'))  # Redireciona para uma página de sucesso
        
        return render_template('cadastro.html', form=form)
