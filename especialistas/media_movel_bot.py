import logging

def calcular_ema(closes, periodo=7):
    k = 2 / (periodo + 1)
    ema = closes[0]
    for price in closes[1:]:
        ema = price * k + ema * (1 - k)
    return ema

def analisar_sinal(candles):
    """
    Retorna:
      - "long" se a EMA(7) cruzou acima da EMA(15),
      - "short" se cruzou abaixo,
      - False caso contrário ou em erro.
    """
    try:
        # valida entrada
        if not isinstance(candles, list) or len(candles) < 15:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        # extrai preços de fechamento
        closes = []
        for c in candles:
            if isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) > 4:
                closes.append(float(c[4]))
            else:
                raise ValueError("Formato de candle inválido.")
        # calcula EMAs
        ema_curta = calcular_ema(closes[-7:], periodo=7)
        ema_longa = calcular_ema(closes[-15:], periodo=15)
        # sinal
        if ema_curta > ema_longa:
            return "long"
        elif ema_curta < ema_longa:
            return "short"
        else:
            return False
    except Exception as e:
        logging.error(f"[especialista_media_movel] {e}")
        return False