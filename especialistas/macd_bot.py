# especialistas/macd_bot.py
import logging

def analisar_macd(candles, par):
    """
    Sinaliza 'long' no cruzamento de alta do MACD (12−26) com sua signal line (9),
    'short' no cruzamento de baixa, ou False em caso contrário ou erro.
    """
    try:
        # precisa de ao menos 35 candles para EMA(26)+signal(9)
        if not isinstance(candles, list) or len(candles) < 35:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        # extrai closes
        closes = []
        for c in candles:
            if isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) > 4:
                closes.append(float(c[4]))
            else:
                raise ValueError("Formato de candle inválido.")
        # função EMA
        def ema(vals, period):
            k = 2 / (period + 1)
            ema_vals = [sum(vals[:period]) / period]
            for price in vals[period:]:
                ema_vals.append(price * k + ema_vals[-1] * (1 - k))
            return ema_vals
        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        # alinha comprimentos
        minlen = min(len(ema12), len(ema26))
        macd_line = [ema12[i] - ema26[i] for i in range(-minlen, 0)]
        signal_line = ema(macd_line, 9)
        # cruzamentos
        if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
            return "long"
        if macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
            return "short"
        return False
    except Exception as e:
        logging.error(f"[especialista_macd] {e}")
        return False