def analisar_sinal(candles):
    """
    Analisa médias móveis simples de 9 e 21 períodos para detectar cruzamentos de tendência.
    Retorna "compra", "venda" ou None.
    """
    if len(candles) < 21:
        return None

    closes = [c['close'] for c in candles]

    sma_9 = sum(closes[-9:]) / 9
    sma_21 = sum(closes[-21:]) / 21

    if sma_9 > sma_21:
        return "compra"
    elif sma_9 < sma_21:
        return "venda"
    else:
        return None