import math

def calcular_poupanca_mensal_com_patrimonio(idade_atual, idade_aposentadoria, renda_desejada_aposentadoria, inflacao_anual, rentabilidade_mensal, patrimonio_atual):
    # Cálculo do número de meses até a aposentadoria
    meses_ate_aposentadoria = (idade_aposentadoria - idade_atual) * 12

    # Ajuste da renda desejada pela inflação ao longo dos anos até a aposentadoria
    inflacao_mensal = (1 + inflacao_anual) ** (1/12) - 1  # Inflação mensal
    renda_aposentadoria_ajustada = renda_desejada_aposentadoria * (1 + inflacao_mensal) ** meses_ate_aposentadoria

    # Fórmula do valor futuro para calcular o valor necessário acumulado
    # Supondo que a pessoa viverá 30 anos após a aposentadoria
    meses_aposentadoria = 30 * 12
    fator_aposentadoria = (1 - (1 + rentabilidade_mensal) ** -meses_aposentadoria) / rentabilidade_mensal
    valor_necessario_aposentadoria = renda_aposentadoria_ajustada * fator_aposentadoria

    # Subtrair o patrimônio atual do valor necessário
    valor_a_ser_acumulado = max(0, valor_necessario_aposentadoria - patrimonio_atual)

    # Fórmula do valor futuro de uma série de pagamentos para calcular a poupança mensal necessária
    fator_poupanca = (1 + rentabilidade_mensal) ** meses_ate_aposentadoria - 1
    poupanca_mensal = valor_a_ser_acumulado / (fator_poupanca / rentabilidade_mensal)

    return poupanca_mensal, valor_a_ser_acumulado, valor_necessario_aposentadoria
