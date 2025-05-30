# especialistas/media_movel_bot.py
import logging

def analisar_media_movel(candles):
    """
    Especialista de cruzamento de EMAs (7 vs 15).
    Retorna 'long' se EMA7 > EMA15, 'short' se EMA7 < EMA15, ou False.
    """
    try:
        # valida entrada
        if not isinstance(candles, list) or len(candles) < 15:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        # extrai fechamento
        closes = []
        for c in candles:
            if isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) > 4:
                closes.append(float(c[4]))
            else:
                raise ValueError("Formato de candle inválido.")
        # calcula EMA
        def ema(values, period):
            k = 2 / (period + 1)
            e = values[0]
            for price in values[1:]:
                e = price * k + e * (1 - k)
            return e
        ema7  = ema(closes[-7:], 7)
        ema15 = ema(closes[-15:], 15)
        # sinal
        if ema7 > ema15:
            return "long"
        if ema7 < ema15:
            return "short"
        return False
    except Exception as e:
        logging.error(f"[especialista_media_movel] {e}")
        return False