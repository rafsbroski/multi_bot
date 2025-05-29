def avaliar_price_action(candles):
    if len(candles) < 10:
        return False

    closes = [float(c["close"]) for c in candles]
    ultimos = closes[-3:]

    return ultimos[2] > ultimos[1] > ultimos[0]