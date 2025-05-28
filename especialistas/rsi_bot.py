def calcular_rsi(closes, periodo=10):  # Período mais curto para candles 5m
    ganhos = 0
    perdas = 0
    for i in range(1, periodo + 1):
        delta = closes[-i] - closes[-i - 1]
        if delta > 0:
            ganhos += delta
        else:
            perdas -= delta
    if perdas == 0:
        return 100
    rs = ganhos / perdas
    rsi = 100 - (100 / (1 + rs))
    return rsi

def avaliar_rsi(candles):
    closes = [float(c[4]) for c in candles]
    if len(closes) < 11:
        return "Hold"
    rsi = calcular_rsi(closes)
    if rsi > 64:
        return "Sell"
    elif rsi < 36:
        return "Buy"
    else:
        return "Hold"