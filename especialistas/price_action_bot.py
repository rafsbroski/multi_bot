# especialistas/price_action_bot.py

def analisar_sinal(candles):
    """
    Analisa padrões de candlestick simples (engolfo e corpo mínimo)
    para gerar sinais de compra ("compra"), venda ("venda") ou None.
    """
    if len(candles) < 2:
        return None

    c1 = candles[-2]
    c2 = candles[-1]

    abertura_1, fechamento_1 = c1['open'], c1['close']
    abertura_2, fechamento_2 = c2['open'], c2['close']

    corpo_1 = abs(fechamento_1 - abertura_1)
    corpo_2 = abs(fechamento_2 - abertura_2)

    # Engolfo de alta
    if fechamento_1 < abertura_1 and fechamento_2 > abertura_2 and abertura_2 < fechamento_1 and fechamento_2 > abertura_1:
        return "compra"

    # Engolfo de baixa
    if fechamento_1 > abertura_1 and fechamento_2 < abertura_2 and abertura_2 > fechamento_1 and fechamento_2 < abertura_1:
        return "venda"

    # Caso nenhum padrão seja detectado
    return None