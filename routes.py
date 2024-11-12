import random
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from calculate_aposentadoria import calcular_poupanca_mensal_com_patrimonio
from models import User, CadastroInicial  # Importar o modelo de usuário e cadastro
from forms import CadastroInicialForm, LoginForm, PrimeiroAcessoForm
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
    def home():
        if not current_user.is_authenticated:
            flash('Faça login para acessar a página.', 'danger')
            return redirect(url_for('login'))
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
            
            idade_atual = form.idade.data
            idade_aposentadoria = form.idade_desejada_aposentadoria.data

            # Criar novo cadastro
            novo_cadastro = CadastroInicial(
                nome_completo=form.nome_completo.data,
                idade=idade_atual,
                renda_mensal=renda_mensal,
                despesas_mensais=despesas_mensais,
                patrimonio_atual=patrimonio_atual,
                idade_desejada_aposentadoria=idade_aposentadoria,
                renda_desejada_aposentadoria=renda_desejada_aposentadoria,
                tolerancia_risco=form.tolerancia_risco.data,
                horizonte_investimentos=form.horizonte_investimentos.data
            )
            
            db.session.add(novo_cadastro)
            db.session.commit()

            return redirect(url_for('home'))  # Redireciona para a página inicial

        return render_template('cadastro.html', form=form)

    def format_brl(value):
        """
        Formata um número para o padrão de moeda brasileiro (R$ x.xxx,xx).
        """
        if value is None:
            return 'R$ 0,00'
        try:
            value = float(value)
        except (ValueError, TypeError):
            return 'R$ 0,00'
        
        # Formata o número com duas casas decimais, substituindo pontos por vírgulas e adicionando separadores de milhares
        formatted = f"R$ {value:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        return formatted

    @app.route('/simulador_aposentadoria', methods=['GET', 'POST'])
    @login_required
    def simulador_aposentadoria():
        # Carregar os dados do usuário atual
        cadastro = CadastroInicial.query.filter_by(nome_completo=current_user.username).first()

        if cadastro is None:
            # Caso o cadastro não seja encontrado, redireciona o usuário para a página de cadastro
            flash('Nenhum cadastro encontrado. Por favor, preencha o cadastro inicial primeiro.', 'danger')
            return redirect(url_for('cadastro'))

        # Pré-preencher o formulário com os dados existentes
        form = CadastroInicialForm(
            nome_completo=cadastro.nome_completo,
            idade=cadastro.idade,
            renda_mensal=cadastro.renda_mensal,
            despesas_mensais=cadastro.despesas_mensais,
            patrimonio_atual=cadastro.patrimonio_atual,
            idade_desejada_aposentadoria=cadastro.idade_desejada_aposentadoria,
            renda_desejada_aposentadoria=cadastro.renda_desejada_aposentadoria,
            tolerancia_risco=cadastro.tolerancia_risco,
            horizonte_investimentos=cadastro.horizonte_investimentos
        )
        
        feedback = None  # Inicializa a variável feedback

        if form.validate_on_submit():
            # Limpar os valores monetários usando a função de formatação
            renda_mensal = format_currency(form.renda_mensal.data)
            despesas_mensais = format_currency(form.despesas_mensais.data)
            patrimonio_atual = format_currency(form.patrimonio_atual.data)
            renda_desejada_aposentadoria = format_currency(form.renda_desejada_aposentadoria.data)
            
            idade_atual = form.idade.data
            idade_aposentadoria = form.idade_desejada_aposentadoria.data
            tolerancia_risco = form.tolerancia_risco.data

            # Definir a rentabilidade mensal com base na tolerância ao risco
            # Definir a rentabilidade mensal com base na tolerância ao risco
            if tolerancia_risco == 'baixo':
                rentabilidade_mensal = 0.008  # 0,3% ao mês
                tipo_investimento = "Investimento Conservador (equivalente ao CDI)"
            elif tolerancia_risco == 'medio':
                rentabilidade_mensal = 0.01  # 0,5% ao mês
                tipo_investimento = "Investimento Moderado (50% em Ações e 50% em CDI)"
            elif tolerancia_risco == 'alto':
                rentabilidade_mensal = 0.012  # 0,7% ao mês
                tipo_investimento = "Investimento Agressivo (predominância em Ações)"
            else:
                rentabilidade_mensal = 0.003
                tipo_investimento = "Investimento Conservador (equivalente ao CDI)"


            inflacao_anual = 0.04  # 4% ao ano
            
            # Cálculo do quanto a pessoa precisa poupar por mês, considerando o patrimônio atual
            poupanca_mensal, valor_a_ser_acumulado, valor_necessario_aposentadoria, patrimonio_futuro = calcular_poupanca_mensal_com_patrimonio(
                idade_atual, 
                idade_aposentadoria, 
                renda_desejada_aposentadoria, 
                inflacao_anual, 
                rentabilidade_mensal, 
                patrimonio_atual
            )
            
            # Formatação dos valores para exibição
            poupanca_mensal_formatada = format_brl(poupanca_mensal)
            valor_necessario_formatado = format_brl(valor_necessario_aposentadoria)
            patrimonio_futuro_formatado = format_brl(patrimonio_futuro)
            valor_a_ser_acumulado_formatado = format_brl(valor_a_ser_acumulado)
            
            # Cálculo da renda disponível para poupança
            renda_disponivel = renda_mensal - despesas_mensais
            renda_disponivel_formatada = format_brl(renda_disponivel)
            
            # Determinação da viabilidade baseada na renda disponível
            if renda_disponivel >= poupanca_mensal:
                viabilidade = "Viável"
                recomendacao = (
                    "Com sua renda atual e despesas, você pode atingir sua renda desejada na aposentadoria. "
                    f"Você precisa guardar {poupanca_mensal_formatada} por mês, aumentando essa poupança anualmente conforme a inflação, "
                    f"até a idade de {idade_aposentadoria} para acumular o valor necessário de {valor_necessario_formatado}.\n\n"
                    f"Estratégia de Investimento Considerada: {tipo_investimento}. A rentabilidade mensal utilizada foi de "
                    f"{rentabilidade_mensal * 100:.2f}%."
                )
            else:
                viabilidade = "Não Viável"
                recomendacao = (
                    f"Considerando sua renda disponível de {renda_disponivel_formatada}, não é possível poupar o suficiente para atingir sua "
                    f"renda desejada de {format_brl(renda_desejada_aposentadoria)} na aposentadoria. Você precisaria poupar {poupanca_mensal_formatada} "
                    f"por mês.\n\n"
                    f"Estratégia de Investimento Considerada: {tipo_investimento}. A rentabilidade mensal utilizada foi de "
                    f"{rentabilidade_mensal * 100:.2f}%."
                )
            
            # Criação do relatório com todas as informações
            feedback = {
                'idade_atual': idade_atual,
                'idade_aposentadoria': idade_aposentadoria,
                'renda_mensal': format_brl(renda_mensal),
                'despesas_mensais': format_brl(despesas_mensais),
                'renda_disponivel': renda_disponivel_formatada,
                'patrimonio_atual': format_brl(patrimonio_atual),
                'patrimonio_futuro': patrimonio_futuro_formatado,
                'renda_desejada_aposentadoria': format_brl(renda_desejada_aposentadoria),
                'valor_necessario_aposentadoria': valor_necessario_formatado,
                'valor_a_ser_acumulado': valor_a_ser_acumulado_formatado,
                'poupanca_mensal': poupanca_mensal_formatada,
                'viabilidade': viabilidade,
                'recomendacao': recomendacao,
                'tipo_investimento': tipo_investimento,
                'rentabilidade_mensal': f"{rentabilidade_mensal * 100:.2f}% ao mês"
            }

            # Atualizar o cadastro com os novos dados
            cadastro.nome_completo = form.nome_completo.data
            cadastro.idade = idade_atual
            cadastro.renda_mensal = renda_mensal
            cadastro.despesas_mensais = despesas_mensais
            cadastro.patrimonio_atual = patrimonio_atual
            cadastro.idade_desejada_aposentadoria = idade_aposentadoria
            cadastro.renda_desejada_aposentadoria = renda_desejada_aposentadoria
            cadastro.tolerancia_risco = tolerancia_risco
            cadastro.horizonte_investimentos = form.horizonte_investimentos.data

            db.session.commit()

            # Passar o feedback para o template
            return render_template('simulador_aposentadoria.html', form=form, feedback=feedback)
        
        return render_template('simulador_aposentadoria.html', form=form, feedback=feedback)
