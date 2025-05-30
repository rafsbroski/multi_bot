import logging

def analisar_sinal(candles):
    """
    Engolfo de alta/baixa simples:
      - "long" para Bullish Engulfing
      - "short" para Bearish Engulfing
      - False caso contrário ou erro
    """
    try:
        # precisa de pelo menos 2 candles
        if not isinstance(candles, list) or len(candles) < 2:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        # pega os dois últimos
        last = candles[-1]
        prev = candles[-2]
        # normaliza open/close/low/high
        def norm(c, key):
            if isinstance(c, dict) and key in c:
                return float(c[key])
            elif isinstance(c, (list, tuple)):
                idx = {"open":1,"high":2,"low":3,"close":4}[key]
                return float(c[idx])
            else:
                raise ValueError("Formato de candle inválido.")
        o1, c1 = norm(prev,"open"), norm(prev,"close")
        o2, c2 = norm(last,"open"), norm(last,"close")
        # Bullish Engulfing
        if c1 < o1 and c2 > o2 and o2 < c1 and c2 > o1:
            return "long"
        # Bearish Engulfing
        if c1 > o1 and c2 < o2 and o2 > c1 and c2 < o1:
            return "short"
        return False
    except Exception as e:
        logging.error(f"[especialista_price_action] {e}")
        return False