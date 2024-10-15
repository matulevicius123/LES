from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange # Adicione as importações necessárias

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class PrimeiroAcessoForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    repeat_password = PasswordField('Repita a Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')])


class CadastroInicialForm(FlaskForm):
    # Informações Pessoais
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    idade = IntegerField('Idade', validators=[DataRequired(), NumberRange(min=18, max=100)])

    # Informações Financeiras
    renda_mensal = DecimalField('Renda Mensal (R$)', validators=[DataRequired()])
    despesas_mensais = DecimalField('Despesas Mensais (R$)', validators=[DataRequired()])
    patrimonio_atual = DecimalField('Patrimônio Atual (R$)', validators=[DataRequired()])
    
    # Aposentadoria
    idade_desejada_aposentadoria = IntegerField('Idade Desejada para Aposentadoria', validators=[DataRequired(), NumberRange(min=30, max=100)])
    renda_desejada_aposentadoria = DecimalField('Renda Mensal Desejada na Aposentadoria (R$)', validators=[DataRequired()])
    
    # Perfil Financeiro
    tolerancia_risco = SelectField('Tolerância ao Risco', choices=[('baixo', 'Baixo'), ('medio', 'Médio'), ('alto', 'Alto')], validators=[DataRequired()])
    horizonte_investimentos = SelectField('Horizonte de Investimento', choices=[('curto_prazo', 'Curto Prazo (1-3 anos)'), ('medio_prazo', 'Médio Prazo (3-7 anos)'), ('longo_prazo', 'Longo Prazo (7+ anos)')], validators=[DataRequired()])
    
    # Metas Financeiras
    meta_financeira_1 = StringField('Meta Financeira (Ex: Comprar uma casa, Viajar)', validators=[DataRequired()])
    valor_meta_1 = DecimalField('Valor da Meta (R$)', validators=[DataRequired()])
    prazo_meta_1 = IntegerField('Prazo em Anos para Alcançar a Meta', validators=[DataRequired(), NumberRange(min=1, max=30)])

    # Submeter
    submit = SubmitField('Enviar')
