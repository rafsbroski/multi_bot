# price_action_bot.py

import logging

def avaliar_price_action(candles):
    try:
        if len(candles) < 2:
            raise ValueError("candles insuficientes")
        c1 = candles[-2]
        c2 = candles[-1]
        o1, h1, l1, c1c = map(float, (c1["open"], c1["high"], c1["low"], c1["close"]))
        o2, h2, l2, c2c = map(float, (c2["open"], c2["high"], c2["low"], c2["close"]))
        # engolfo
        if c1c < o1 and c2c > o2 and o2 < c1c and c2c > o1:
            return "buy"
        if c1c > o1 and c2c < o2 and o2 > c1c and c2c < o1:
            return "sell"
        # fallback por cor do candle
        return "buy" if c2c > o2 else "sell" if c2c < o2 else None
    except Exception as e:
        logging.error(f"especialista_price_action: Estrutura de candles inválida ou insuficiente. {e}")
        return None