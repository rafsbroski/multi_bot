def calcular_ema(closes, periodo=7):
    k = 2 / (periodo + 1)
    ema = closes[0]
    for preco in closes[1:]:
        ema = preco * k + ema * (1 - k)
    return ema

def avaliar_media_movel(candles):
    closes = [float(c[4]) for c in candles]
    if len(closes) < 15:
        return "Hold"
    ema_curta = calcular_ema(closes[-7:], periodo=7)
    ema_longa = calcular_ema(closes[-15:], periodo=15)

    if ema_curta > ema_longa:
        return "Buy"
    elif ema_curta < ema_longa:
        return "Sell"
    else:
        return "Hold"