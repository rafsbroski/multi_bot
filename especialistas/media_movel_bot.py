import logging

def analisar_media_movel(candles, par):
    try:
        if not isinstance(candles, list) or len(candles) < 21:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")

        closes = []
        for c in candles:
            if not isinstance(c, dict):
                raise ValueError("Candle não é um dicionário.")
            if not all(k in c for k in ["open", "high", "low", "close", "volume", "timestamp"]):
                raise ValueError("Candle com campos incompletos.")
            closes.append(float(c["close"]))

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