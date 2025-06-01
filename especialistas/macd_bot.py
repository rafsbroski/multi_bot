import logging

def analisar_macd(candles, par):
    try:
        if not isinstance(candles, list) or len(candles) < 35:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")

        closes = []
        for c in candles:
            if isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) > 4:
                closes.append(float(c[4]))
            else:
                raise ValueError("Formato de candle inválido.")

        def ema(data, period):
            multiplier = 2 / (period + 1)
            ema_values = [sum(data[:period]) / period]
            for price in data[period:]:
                ema_values.append((price - ema_values[-1]) * multiplier + ema_values[-1])
            return ema_values

        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        if len(ema26) < len(ema12):
            ema12 = ema12[-len(ema26):]
        macd_line = [a - b for a, b in zip(ema12, ema26)]
        signal_line = ema(macd_line, 9)

        if len(signal_line) < 2:
            return None

        if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]:
            return "long"
        elif macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]:
            return "short"
        return None

    except Exception as e:
        logging.error(f"[especialista_macd] {e}")
        return None