def avaliar_volume(candles):
    volumes = [float(c[5]) for c in candles]
    media_volume = sum(volumes) / len(volumes)
    ultimo_volume = volumes[-1]

    fator_threshold = 1.08  # Menos exigente (8% acima da média para Buy)
    if ultimo_volume > media_volume * fator_threshold:
        return "Buy"
    elif ultimo_volume < media_volume / fator_threshold:
        return "Sell"
    else:
        return "Hold"