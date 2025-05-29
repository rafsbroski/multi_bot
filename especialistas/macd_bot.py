def analisar_macd(candles):
    if len(candles) < 35:
        return False  # precisamos de pelo menos 35 candles

    closes = [c['close'] for c in candles]

    # MACD: EMA12 e EMA26
    def ema(values, period):
        k = 2 / (period + 1)
        ema_values = [sum(values[:period]) / period]
        for price in values[period:]:
            ema_values.append(price * k + ema_values[-1] * (1 - k))
        return ema_values

    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)

    # alinhar os comprimentos
    min_len = min(len(ema12), len(ema26))
    macd_line = [ema12[i] - ema26[i] for i in range(-min_len, 0)]

    signal_line = ema(macd_line, 9)

    # cruzamento de alta
    if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
        return "compra"
    
    # cruzamento de baixa
    elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
        return "venda"

    return False