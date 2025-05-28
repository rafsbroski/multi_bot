def avaliar_momentum(candles):
    closes = [float(c[4]) for c in candles]
    if len(closes) < 5:
        return "Hold"
    # Calcula momentum dos últimos 2 períodos (mais rápido)
    momentums = []
    for i in range(-2, 0):
        momentums.append(closes[i] - closes[i - 1])
    momentum_medio = sum(momentums) / len(momentums)

    if momentum_medio > 0:
        return "Buy"
    elif momentum_medio < 0:
        return "Sell"
    else:
        return "Hold"