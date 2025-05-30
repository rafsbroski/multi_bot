import logging

def analisar_price_action(candles, par):
    try:
        if not isinstance(candles, list) or len(candles) < 5:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        closes = []
        for c in candles:
            if isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) > 4:
                closes.append(float(c[4]))
            else:
                raise ValueError("Formato de candle inválido.")

        if closes[-1] > max(closes[-5:-1]):
            return "long"
        elif closes[-1] < min(closes[-5:-1]):
            return "short"
        else:
            return False

    except Exception as e:
        logging.error(f"[especialista_price_action] {e}")
        return False