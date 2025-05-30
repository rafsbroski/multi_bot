# macd_bot.py

import logging

def analisar_macd(candles):
    try:
        closes = [float(c["close"]) for c in candles]
        if len(closes) < 26:
            raise ValueError("candles insuficientes")
        # função EMA genérica
        def ema(vals, per):
            k = 2 / (per + 1)
            ema_list = [sum(vals[:per]) / per]
            for price in vals[per:]:
                ema_list.append(price * k + ema_list[-1] * (1 - k))
            return ema_list
        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        # alinhamento
        minlen = min(len(ema12), len(ema26))
        macd_line = [ema12[-i] - ema26[-i] for i in range(1, minlen+1)]
        signal = ema(macd_line, 9)
        if macd_line[-2] < signal[-2] < macd_line[-1] > signal[-1]:
            return "buy"
        if macd_line[-2] > signal[-2] > macd_line[-1] < signal[-1]:
            return "sell"
        return None
    except Exception as e:
        logging.error(f"especialista_macd: Estrutura de candles inválida ou insuficiente. {e}")
        return None