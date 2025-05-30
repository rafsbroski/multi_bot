# especialistas/price_action_bot.py
import logging

def avaliar_price_action(candles):
    """
    Especialista de padrão de candle:
    Engolfos, martelo e estrela cadente.
    Retorna 'long' ou 'short', ou False.
    """
    try:
        if not isinstance(candles, list) or len(candles) < 2:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        # pega últimos dois
        c1, c2 = candles[-2], candles[-1]
        # extrai campos
        def get(o, key):
            if isinstance(o, dict) and key in o:
                return float(o[key])
            elif isinstance(o, (list, tuple)):
                # [0]=ts, [1]=open, [2]=high, [3]=low, [4]=close, [5]=volume
                idx = {"open":1,"high":2,"low":3,"close":4}[key]
                return float(o[idx])
            else:
                raise ValueError("Formato de candle inválido.")
        o1, h1, l1, c1v = get(c1,"open"), get(c1,"high"), get(c1,"low"), get(c1,"close")
        o2, h2, l2, c2v = get(c2,"open"), get(c2,"high"), get(c2,"low"), get(c2,"close")
        # Engolfo de alta
        if c1v < o1 and c2v > o2 and o2 < c1v and c2v > o1:
            return "long"
        # Engolfo de baixa
        if c1v > o1 and c2v < o2 and o2 > c1v and c2v < o1:
            return "short"
        # Martelo / Hammer
        body = abs(c2v - o2)
        lower_shadow = (o2 - l2) if o2 > c2v else (c2v - l2)
        if body > 0 and lower_shadow > 2 * body and (h2 - max(c2v, o2)) < body:
            return "long"
        # Estrela cadente
        upper_shadow = h2 - max(c2v, o2)
        if body > 0 and upper_shadow > 2 * body and (min(c2v, o2) - l2) < body:
            return "short"
        return False
    except Exception as e:
        logging.error(f"[especialista_price_action] {e}")
        return False