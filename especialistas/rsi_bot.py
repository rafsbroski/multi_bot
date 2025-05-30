# rsi_bot.py

import logging

def calcular_rsi(closes, periodo=14):
    gains = losses = 0.0
    for i in range(1, periodo+1):
        delta = closes[-i] - closes[-i-1]
        gains  += delta if delta>0 else 0
        losses += -delta if delta<0 else 0
    if losses == 0:
        return 100
    rs  = gains / losses
    return 100 - (100 / (1 + rs))

def avaliar_rsi(candles):
    try:
        closes = [float(c["close"]) for c in candles]
        if len(closes) < 15:
            raise ValueError("candles insuficientes")
        rsi = calcular_rsi(closes[-15:], 14)
        return "buy" if rsi < 30 else "sell" if rsi > 70 else None
    except Exception as e:
        logging.error(f"especialista_rsi: Estrutura de candles inválida ou insuficiente. {e}")
        return None
