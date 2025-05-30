import logging

def avaliar_price_action(candles):
    """
    Sinal de price action:
    - Engolfo de alta/baixa
    - Martelo / Estrela cadente
    Retorna 'long', 'short' ou None. Proteção contra entradas inválidas.
    """
    try:
        # Verifica lista e tamanho mínimo
        if not isinstance(candles, list) or len(candles) < 2:
            raise ValueError("Candles insuficientes")
        c1 = candles[-2]
        c2 = candles[-1]
        o1, c1c = float(c1["open"]), float(c1["close"])
        o2, c2c = float(c2["open"]), float(c2["close"])
        low2, high2 = float(c2["low"]), float(c2["high"])

        # Engolfo de alta
        if c1c < o1 and c2c > o2 and o2 < c1c and c2c > o1:
            return "long"
        # Engolfo de baixa
        if c1c > o1 and c2c < o2 and o2 > c1c and c2c < o1:
            return "short"

        corpo = abs(c2c - o2)
        # Martelo
        sombra_inf = (o2 - low2) if o2 > c2c else (c2c - low2)
        if corpo > 0 and sombra_inf > 2 * corpo and (high2 - max(c2c, o2)) < corpo:
            return "long"
        # Estrela cadente
        sombra_sup = high2 - max(c2c, o2)
        if corpo > 0 and sombra_sup > 2 * corpo and (min(c2c, o2) - low2) < corpo:
            return "short"

        return None
    except Exception:
        logging.error("especialista_price_action: Estrutura de candles inválida ou insuficiente.")
        return None