import math

def calcular_poupanca_mensal_com_patrimonio(idade_atual, idade_aposentadoria, renda_desejada_aposentadoria, inflacao_anual, rentabilidade_mensal, patrimonio_atual):
    # Cálculo do número de meses até a aposentadoria
    meses_ate_aposentadoria = (idade_aposentadoria - idade_atual) * 12

    # Ajuste da renda desejada pela inflação ao longo dos anos até a aposentadoria
    inflacao_mensal = (1 + inflacao_anual) ** (1/12) - 1  # Inflação mensal
    renda_aposentadoria_ajustada = renda_desejada_aposentadoria * (1 + inflacao_mensal) ** meses_ate_aposentadoria

    # Ajuste do patrimônio atual pela rentabilidade mensal ao longo do tempo
    patrimonio_futuro = patrimonio_atual * (1 + rentabilidade_mensal) ** meses_ate_aposentadoria

    # Fórmula do valor futuro para calcular o valor necessário acumulado
    # Supondo que a pessoa viverá 30 anos após a aposentadoria
    meses_aposentadoria = 30 * 12
    fator_aposentadoria = (1 - (1 + rentabilidade_mensal) ** -meses_aposentadoria) / rentabilidade_mensal
    valor_necessario_aposentadoria = renda_aposentadoria_ajustada * fator_aposentadoria

    # Subtrair o patrimônio futuro do valor necessário
    valor_a_ser_acumulado = max(0, valor_necessario_aposentadoria - patrimonio_futuro)

    if valor_a_ser_acumulado == 0:
        poupanca_mensal = 0
    else:
        # Fórmula do valor futuro de uma série de pagamentos para calcular a poupança mensal necessária
        fator_poupanca = ((1 + rentabilidade_mensal) ** meses_ate_aposentadoria - 1) / rentabilidade_mensal
        poupanca_mensal = valor_a_ser_acumulado / fator_poupanca

    return poupanca_mensal, valor_a_ser_acumulado, valor_necessario_aposentadoria, patrimonio_futuro
