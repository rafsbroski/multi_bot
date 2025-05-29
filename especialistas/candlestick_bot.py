def analisar_sinal(candles):
    if len(candles) < 2:
        return False

    c1 = candles[-2]
    c2 = candles[-1]

    # Engolfo de alta
    if c1['close'] < c1['open'] and c2['close'] > c2['open'] and c2['open'] < c1['close'] and c2['close'] > c1['open']:
        return "compra"

    # Engolfo de baixa
    if c1['close'] > c1['open'] and c2['close'] < c2['open'] and c2['open'] > c1['close'] and c2['close'] < c1['open']:
        return "venda"

    # Martelo (hammer)
    corpo = abs(c2['close'] - c2['open'])
    sombra_inferior = c2['open'] - c2['low'] if c2['open'] > c2['close'] else c2['close'] - c2['low']
    if corpo > 0 and sombra_inferior > 2 * corpo and c2['high'] - max(c2['close'], c2['open']) < corpo:
        return "compra"

    # Estrela cadente
    sombra_superior = c2['high'] - max(c2['close'], c2['open'])
    if corpo > 0 and sombra_superior > 2 * corpo and min(c2['close'], c2['open']) - c2['low'] < corpo:
        return "venda"

    return False
