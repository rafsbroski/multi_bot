import logging

def analisar_rsi(candles, par):
    try:
        if not isinstance(candles, list) or len(candles) < 15:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        closes = []
        for c in candles:
            if isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) > 4:
                closes.append(float(c[4]))
            else:
                raise ValueError("Formato de candle inválido.")

        deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        avg_gain = sum(gains[-14:]) / 14
        avg_loss = sum(losses[-14:]) / 14
        if avg_loss == 0:
            return "long"
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        if rsi < 30:
            return "long"
        if rsi > 70:
            return "short"
        return None

    except Exception as e:
        logging.error(f"[especialista_rsi] {e}")
        return None