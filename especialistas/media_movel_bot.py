import logging

def avaliar_media_movel(candles):
    """
    Retorna 'long' se EMA7 > EMA15, 'short' se EMA7 < EMA15, ou None caso contrário.
    Proteção contra entradas inválidas ou candles insuficientes.
    """
    try:
        # Verifica lista e tamanho mínimo
        if not isinstance(candles, list) or len(candles) < 15:
            raise ValueError("Candles insuficientes")
        # Extrai closes
        closes = [float(c["close"]) for c in candles]
        # Função para calcular EMA
        def _ema(prices, period):
            k = 2 / (period + 1)
            ema = prices[0]
            for price in prices[1:]:
                ema = price * k + ema * (1 - k)
            return ema
        ema7 = _ema(closes[-7:], 7)
        ema15 = _ema(closes[-15:], 15)
        if ema7 > ema15:
            return "long"
        elif ema7 < ema15:
            return "short"
        else:
            return None
    except Exception:
        logging.error("especialista_media_movel: Estrutura de candles inválida ou insuficiente.")
        return None