import logging

def analisar_media(candles, par):
    try:
        if not isinstance(candles, list) or len(candles) < 21:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        closes = []
        for c in candles:
            if isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) > 4:
                closes.append(float(c[4]))
            else:
                raise ValueError("Formato de candle inválido.")

        sma_9 = sum(closes[-9:]) / 9
        sma_21 = sum(closes[-21:]) / 21
        if sma_9 > sma_21:
            return "long"
        elif sma_9 < sma_21:
            return "short"
        else:
            return False

    except Exception as e:
        logging.error(f"[especialista_media_movel] {e}")
        return False