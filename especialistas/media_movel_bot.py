def analisar_mercado(candles):
    if len(candles) < 50:
        return False

    soma_curta = sum(c["close"] for c in candles[-9:])
    media_curta = soma_curta / 9

    soma_longa = sum(c["close"] for c in candles[-50:])
    media_longa = soma_longa / 50

    return media_curta > media_longa or media_curta < media_longa
