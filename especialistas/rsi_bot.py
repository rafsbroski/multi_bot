def analisar_mercado(candles):
    if len(candles) < 15:
        return False  # Não há dados suficientes para calcular o RSI

    subidas = []
    descidas = []

    for i in range(1, 15):
        dif = candles[-i]["close"] - candles[-i - 1]["close"]
        if dif > 0:
            subidas.append(dif)
            descidas.append(0)
        else:
            subidas.append(0)
            descidas.append(abs(dif))

    media_subidas = sum(subidas) / 14
    media_descidas = sum(descidas) / 14

    if media_descidas == 0:
        return False  # Evitar divisão por zero

    rs = media_subidas / media_descidas
    rsi = 100 - (100 / (1 + rs))

    return rsi < 30 or rsi > 70