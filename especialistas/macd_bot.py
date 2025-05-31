import logging

def analisar_macd(candles, par):
    try:
        if not isinstance(candles, list) or len(candles) < 35:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")

        closes = []
        for c in candles:
            if not isinstance(c, dict):
                raise ValueError("Candle não é um dicionário.")
            if not all(k in c for k in ["open", "high", "low", "close", "volume", "timestamp"]):
                raise ValueError("Candle com campos incompletos.")
            closes.append(float(c["close"]))

        def ema(vals, period):
            k = 2 / (period + 1)
            ema_vals = [sum(vals[:period]) / period]
            for price in vals[period:]:
                ema_vals.append(price * k + ema_vals[-1] * (1 - k))
            return ema_vals

        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        macd_line = [a - b for a, b in zip(ema12[-len(ema26):], ema26)]
        signal_line = ema(macd_line, 9)

        if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
            return "long"
        elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
            return "short"
        else:
            return False

    except Exception as e:
        logging.error(f"[especialista_macd] {e}")
        return False