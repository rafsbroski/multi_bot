# media_movel_bot.py

import logging

def analisar_media_movel(candles):
    try:
        # espera uma lista de dicts com chave "close"
        closes = [float(c["close"]) for c in candles]
        if len(closes) < 15:
            raise ValueError("candles insuficientes")
        # EMA de 7 e 15
        def ema(values, period):
            k = 2 / (period + 1)
            ema_val = values[0]
            for v in values[1:]:
                ema_val = v * k + ema_val * (1 - k)
            return ema_val
        ema7  = ema(closes[-7:], 7)
        ema15 = ema(closes[-15:], 15)
        return "buy" if ema7 > ema15 else "sell" if ema7 < ema15 else None
    except Exception as e:
        logging.error(f"especialista_media_movel: Estrutura de candles inválida ou insuficiente. {e}")
        return None