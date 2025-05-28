def avaliar_price_action(candles):
    if len(candles) < 3:
        return "Hold"
    ultimo_candle = candles[-1]
    penultimo_candle = candles[-2]

    abertura_ult = float(ultimo_candle[1])
    fechamento_ult = float(ultimo_candle[4])
    abertura_pen = float(penultimo_candle[1])
    fechamento_pen = float(penultimo_candle[4])

    corpo_ult = abs(fechamento_ult - abertura_ult)
    corpo_pen = abs(fechamento_pen - abertura_pen)

    # Menos exigente no tamanho do candle
    if corpo_ult < 0.0005 * fechamento_ult:
        return "Hold"

    # Engolfo de alta/baixa mais reativo
    if fechamento_ult > abertura_ult and abertura_ult < fechamento_pen and fechamento_ult > abertura_pen:
        return "Buy"
    elif fechamento_ult < abertura_ult and abertura_ult > fechamento_pen and fechamento_ult < abertura_pen:
        return "Sell"
    else:
        if fechamento_ult > abertura_ult:
            return "Buy"
        elif fechamento_ult < abertura_ult:
            return "Sell"
        else:
            return "Hold"